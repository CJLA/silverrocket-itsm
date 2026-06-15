from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name")

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
