# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile  # 指定模型为UserProfile
        fields = ['avatar']  # 序列化avatar字段
