from rest_framework import serializers
from .models import AppUser

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'

    def validate_email(self, value):
      if AppUser.objects.filter(email=value).exists():
        raise serializers.ValidationError("Email already exists")
      return value
