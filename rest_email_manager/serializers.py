from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import EmailAddress


User = get_user_model()


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ["email"]

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.send_verification()
        return instance

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "A user with this email already exists"
            )

        return email
