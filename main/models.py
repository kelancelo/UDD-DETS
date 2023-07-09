from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Event(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    STATUS_CHOICES = [
        ("active", "active"),
        ("scheduled", "scheduled"),
        ("ended", "ended")
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="scheduled")
    # Field for accessing m2m relationship between Participant
    participants = models.ManyToManyField("Participant", blank=True, through="Event_Participant")
    # Field for accessing m2m relationship between User of type "judge"
    judges = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.name}"


class Round(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    number = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    STATUS_CHOICES = [
        ("active", "active"),
        ("scheduled", "scheduled"),
        ("ended", "ended")
    ]
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default="scheduled")
    num_winners = models.IntegerField(verbose_name="Number of winners", null=True, blank=True)
    # Field for accessing m2m relationship between Participant
    participants = models.ManyToManyField("Participant", blank=True)

    def __str__(self):
        return f"{self.event.name}: {self.name if self.name else 'Round: ' + str(self.number)}"


class Criterion(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    max_score = models.IntegerField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural  =  "Criteria"


class Participant(models.Model):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female")
    ]
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to='main/participant_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Score(models.Model):
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE)
    judge = models.ForeignKey(User, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    value = models.IntegerField()


# Stores the average score of a participant from all judges of a round
class Total_Score(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)


class Represented_Entity(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural  =  "Represented entities"


class Event_Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    candidate_number = models.IntegerField()
    represented_entity = models.ForeignKey(Represented_Entity, on_delete=models.SET_NULL, null=True)
    