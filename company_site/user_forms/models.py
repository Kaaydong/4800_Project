from django.db import models
from django.contrib.auth import get_user_model

class Settings(models.Model):
    settings_id = models.AutoField(primary_key=True)
    user_key = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    max_age_restriction = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user_key) + "'s Settings"  