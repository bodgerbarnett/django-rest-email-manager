from rest_framework import serializers

from .models import EmailAddress


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ["email"]

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.send_verification()
        return instance
