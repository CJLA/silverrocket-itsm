from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import CustomUser


class NormalizedEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return CustomUser.objects.normalize_email(value)


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = NormalizedEmailField(
        validators=[
            UniqueValidator(queryset=CustomUser.objects.all()),
        ],
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name")

    def validate(self, attrs):
        user = CustomUser(
            email=attrs.get("email"),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )

        try:
            validate_password(attrs["password"], user=user)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages}) from error

        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
