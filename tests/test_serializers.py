from rest_email_manager.serializers import CreateEmailAddressSerializer


def test_create_emailaddress(mocker, db, user, api_request):
    mock_send_verification = mocker.patch(
        "rest_email_manager.models.EmailAddress.send_verification"
    )

    data = {"email": "test@example.com", "current_password": "secret"}

    api_request.user = user
    serializer = CreateEmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert serializer.is_valid()

    emailaddress = serializer.save(user=user)

    assert emailaddress.email == data["email"]

    mock_send_verification.assert_called()


def test_no_create_without_password(db):
    data = {"email": "test@example.com"}

    serializer = CreateEmailAddressSerializer(data=data)
    assert not serializer.is_valid()


def test_no_create_with_invalid_password(db, user, api_request):
    data = {"email": "test@example.com", "current_password": "wrong"}

    api_request.user = user
    serializer = CreateEmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert not serializer.is_valid()


def test_no_update_email_to_existing_user_email(db, user, api_request):
    data = {"email": user.email, "current_password": "secret"}

    api_request.user = user
    serializer = CreateEmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"email"}
