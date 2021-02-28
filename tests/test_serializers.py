from unittest import mock

from rest_email_manager.serializers import EmailAddressSerializer


@mock.patch(
    "rest_email_manager.models.EmailAddress.send_verification",
    autospec=True,
)
def test_create_emailaddress(mock_send_verification, db, user, api_request):
    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_request.user = user
    serializer = EmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert serializer.is_valid()

    emailaddress = serializer.save(user=user)

    assert emailaddress.email == data["email"]

    mock_send_verification.assert_called()


@mock.patch(
    "rest_email_manager.models.EmailAddress.send_verification",
    autospec=True,
)
def test_create_emailaddress_duplicate_email(mock_send_verification, db, user, email_address_factory, api_request):
    email_address_factory(user=user, email="newemail@example.com")

    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_request.user = user
    serializer = EmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert serializer.is_valid()

    emailaddress = serializer.save(user=user)

    assert emailaddress.email == data["email"]

    mock_send_verification.assert_called()


def test_create_without_email(db):
    data = {"password": "secret"}

    serializer = EmailAddressSerializer(data=data)
    assert not serializer.is_valid()


def test_create_without_password(db):
    data = {"email": "newemail@example.com"}

    serializer = EmailAddressSerializer(data=data)
    assert not serializer.is_valid()


def test_create_with_invalid_password(db, user, api_request):
    data = {"email": "newemail@example.com", "current_password": "wrong"}

    api_request.user = user
    serializer = EmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert not serializer.is_valid()


def test_update_email_to_existing_user_email(db, user, api_request):
    data = {"email": user.email, "current_password": "secret"}

    api_request.user = user
    serializer = EmailAddressSerializer(
        data=data, context={'request': api_request}
    )
    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"email"}
