from django.contrib.auth import get_user_model
from user_forms import models

def getUserById(id):
    return get_user_model().objects.get(id=id)

def getUserSettingsByUser(user):
    return models.Settings.objects.get(user_key=user) 