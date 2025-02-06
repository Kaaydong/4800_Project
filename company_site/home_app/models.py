from django.db import models

# Create your models here.
class MeetingLog(models.Model):
    meeting_name = models.CharField(max_length=256)
    all_meeting_text = models.TextField()
    arnav_present = models.BooleanField(default=True)
    kayden_present = models.BooleanField(default=True)
    ian_present = models.BooleanField(default=True)
    keon_present = models.BooleanField(default=True)
    bao_present = models.BooleanField(default=True)
    date_submitted = models.DateField()

    def __str__(self):
        return self.meeting_name