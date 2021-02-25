from django.core import mail

from rest_email_manager.serializers import EmailAddressSerializer


def test_create_emailaddress(db, user):
    data = {"email": "test@example.com"}

    serializer = EmailAddressSerializer(data=data)
    assert serializer.is_valid()

    emailaddress = serializer.save(user=user)

    assert emailaddress.email == data["email"]
    assert not emailaddress.verified

    assert len(mail.outbox) == 1
