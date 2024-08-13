# models.py
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 创建一个与User模型一对一的关系
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # 创建一个字段来存储用户的头像
