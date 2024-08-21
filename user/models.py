# models.py
from django.contrib.auth.models import User
from django.db import models

from image.models import ImageSave


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ForeignKey(ImageSave, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='头像')
