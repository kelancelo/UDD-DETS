from django import forms
from .models import *
from django.core.exceptions import ObjectDoesNotExist


class EventForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        # print(cleaned_data)
        # if self.instance is None:
        #     round = Round.objects.create(event=self.instance, number=1)
        #     round.start_date = self.instance.start_date
        #     for participant in self.instance.participants.all():
        #         round.participants.add(participant)
        #     round.save()
        if status == "active":
            active_event = None
            try:
                active_event = Event.objects.get(status="active")
            except ObjectDoesNotExist:
                pass
            if active_event and active_event.id != self.instance.pk:
                raise forms.ValidationError("Only 1 event can be active at a time.")

        return cleaned_data


class RoundForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial and self.initial != self.data:
            # Filter participants based on the related event
            self.fields['participants'].queryset = Participant.objects.filter(event=self.instance.event)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        event = cleaned_data.get("event")

        if status == "active":
            if event.status != "active":
                raise forms.ValidationError("To activate this round, activate the event for this round first.")
            else:
                active_round = None
                try:
                    active_round = Round.objects.get(status="active")
                except ObjectDoesNotExist:
                    pass
                if active_round and active_round.id != self.instance.pk:
                    raise forms.ValidationError("Only 1 round can be active at a time.")
        elif status == "ended":
            round = self.instance
            num_judges = event.judges.count()
            for participant in round.participants.all():
                total_score = 0
                scores = Score.objects.filter(criterion__round=round, participant=participant)
                for score in scores:
                    total_score += score.value
                Total_Score.objects.create(
                    round=round, 
                    participant=participant, 
                    value=total_score/num_judges
                )
            if round.num_winners > 1:
                new_round = Round.objects.create(event=event, number=round.number+1)
                round_winners = Total_Score.objects.filter(round=round).order_by("-value")[:round.num_winners]
                for winner in round_winners:
                    new_round.participants.add(winner.participant)
                new_round.save()

        return cleaned_data