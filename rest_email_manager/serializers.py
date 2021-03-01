from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import EmailAddress, EmailAddressVerification


User = get_user_model()


class EmailAddressSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "email_already_exists": "A user with this email already exists",
        "invalid_password": "Invalid password",
    }

    class Meta:
        model = EmailAddress
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["current_password"] = serializers.CharField(
            write_only=True, style={"input_type": "password"}
        )

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            self.fail("email_already_exists")

        return email

    def validate_current_password(self, password):
        if self.context["request"].user.check_password(password):
            return password
        else:
            self.fail("invalid_password")

    def create(self, validated_data):
        validated_data.pop("current_password")

        try:
            instance = self.context["request"].user.emailaddresses.get(
                email=validated_data["email"]
            )
        except EmailAddress.DoesNotExist:
            instance = super().create(validated_data)

        instance.send_verification()
        return instance


class EmailAddressVerificationSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "invalid_key": "Invalid verification key",
    }

    class Meta:
        model = EmailAddressVerification
        fields = ["key"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["key"].required = True

    def validate_key(self, key):
        try:
            self.instance = EmailAddressVerification.objects.exclude(
                emailaddress__email__in=User.objects.values_list(
                    "email", flat=True
                )
            ).get(key=key, emailaddress__user=self.context["request"].user)
        except EmailAddressVerification.DoesNotExist:
            self.fail("invalid_key")

    def save(self):
        self.instance.verify()
