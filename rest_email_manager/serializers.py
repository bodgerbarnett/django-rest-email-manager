from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import EmailAddress


User = get_user_model()


class EmailAddressSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "email_already_exists": "A user with this email already exists"
    }

    class Meta:
        model = EmailAddress
        fields = ["email"]

    def create(self, validated_data):
        validated_data.pop("current_password")
        instance = super().create(validated_data)
        instance.send_verification()
        return instance

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            self.fail("email_already_exists")

        return email


class CurrentPasswordSerializer(serializers.Serializer):
    default_error_messages = {
        "invalid_password": "Invalid password",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["current_password"] = serializers.CharField(
            write_only=True,
            style={"input_type": "password"}
        )

    def validate_current_password(self, password):
        if self.context["request"].user.check_password(
            password
        ):
            return password
        else:
            self.fail("invalid_password")


class CreateEmailAddressSerializer(EmailAddressSerializer, CurrentPasswordSerializer):
    pass
