from rest_email_manager.serializers import EmailAddressSerializer


def test_create_emailaddress(mocker, db, user):
    mock_send_verification = mocker.patch(
        "rest_email_manager.models.EmailAddress.send_verification"
    )

    data = {"email": "test@example.com"}

    serializer = EmailAddressSerializer(data=data)
    assert serializer.is_valid()

    emailaddress = serializer.save(user=user)

    assert emailaddress.email == data["email"]

    mock_send_verification.assert_called()
