from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import EventForm, RoundForm
from django.core.exceptions import ObjectDoesNotExist


admin.site.site_header = "DETS Administration"
admin.site.site_title = "UDD DETS"
admin.site.index_template = 'admin/index.html'

admin.site.register(User, UserAdmin)

class ParticipantInline(admin.TabularInline):
    model = Event.participants.through
    extra = 0

class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields]
    list_filter = ["status"]
    form = EventForm
    inlines = [ParticipantInline]
admin.site.register(Event, EventAdmin)

class RoundAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Round._meta.fields]
    list_filter = ["event", "status"]
    form = RoundForm
admin.site.register(Round, RoundAdmin)

class CriterionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Criterion._meta.fields]
    list_filter = ["round__event", "round"]
admin.site.register(Criterion, CriterionAdmin)

class EventFilter(admin.SimpleListFilter):
    title = "Event"
    parameter_name = "event"

    def lookups(self, request, model_admin):
        events = Event.objects.all()
        return [(event.id, event.name) for event in events]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(event__id=self.value())
        
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Participant._meta.fields]
    list_filter = ["gender", EventFilter]
admin.site.register(Participant, ParticipantAdmin)

class ScoreAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Score._meta.fields]
    list_filter = ["criterion__round__event", "criterion__round"]
    search_fields = ["participant__first_name", "participant__last_name"]

    # def update_total_score(self, form, current_total_score, num_judges, original_obj=None):
    #     new_total_score = current_total_score.value * num_judges
    #     if original_obj:
    #         new_total_score -= original_obj.value
    #     new_total_score += form.cleaned_data["value"]
    #     new_total_score /= num_judges
    #     current_total_score.value = new_total_score
    #     current_total_score.save()

    # def save_model(self, request, obj, form, change):
    #     criterion = Criterion.objects.get(id=obj.criterion_id)
    #     round = Round.objects.get(id=criterion.round_id)
    #     num_judges = Event.objects.get(id=round.event_id).judges.count()
    #     current_total_score = None
    #     try:
    #         current_total_score = Total_Score.objects.get(
    #             participant_id=obj.participant_id,
    #             round=round
    #         )
    #     except ObjectDoesNotExist:
    #         pass
    #     # If the score is being updated 
    #     if change:
    #         original_obj = Score.objects.get(id=obj.id)
    #         self.update_total_score(form, current_total_score, num_judges, original_obj=original_obj)
    #     # if the score is just being created and there's already a total score
    #     elif not change and current_total_score:
    #         self.update_total_score(form, current_total_score, num_judges)
    #     # If the score is just being created and there's still no total score
    #     else:
    #         Total_Score.objects.create(
    #             participant_id=obj.participant_id,
    #             round=round,
    #             value=form.cleaned_data["value"]/num_judges
    #         )
    #     super().save_model(request, obj, form, change)
admin.site.register(Score, ScoreAdmin)

class TotalScoreAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Total_Score._meta.fields]
    search_fields = ["participant__first_name", "participant__last_name"]
    list_filter = ["round__event", "round"]
admin.site.register(Total_Score, TotalScoreAdmin)

class RepresentedEntityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Represented_Entity._meta.fields]
admin.site.register(Represented_Entity, RepresentedEntityAdmin)

