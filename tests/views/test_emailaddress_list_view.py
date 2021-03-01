from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_manager.serializers import EmailAddressSerializer


list_url = reverse("emailaddress-list")


def test_list(db, api_client, user, email_address_factory):
    """
    GET
    returns all user's email addresses
    """
    email_address_factory(user=user, email="one@example.com")
    email_address_factory(user=user, email="two@example.com")

    # create an email address for another user
    email_address_factory()

    serializer = EmailAddressSerializer(user.emailaddresses.all(), many=True)

    api_client.force_authenticate(user=user)
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_list_no_auth(db, api_client):
    """
    GET
    no authentication
    fails with permission denied
    """
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@mock.patch(
    "rest_email_manager.models.EmailAddress.send_verification",
    autospec=True,
)
def test_create(mock_send_verification, db, api_client, user):
    """
    POST
    valid email and password
    creates new EmailAddress and sends verification email
    """
    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_201_CREATED

    serializer = EmailAddressSerializer(user.emailaddresses.get())

    assert response.data == serializer.data

    mock_send_verification.assert_called()


def test_create_no_auth(db, api_client):
    """
    POST
    no authentication
    fails with permission denied
    """
    data = {"email": "newemail@example.com", "current_password": "secret"}
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_no_email(db, api_client, user):
    """
    POST
    no email
    fails with email address required
    """
    data = {"current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_no_password(db, api_client, user):
    """
    POST
    no password
    fails with password required
    """
    data = {"email": "newemail@example.com"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_wrong_password(db, api_client, user):
    """
    POST
    wrong password
    fails
    """
    data = {"email": "newemail@example.com", "current_password": "wrong"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_duplicate_user_email(
    db, api_client, user, user_factory
):
    """
    POST
    email belongs to another user account
    fails
    """
    user_factory(email="newemail@example.com")

    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@mock.patch(
    "rest_email_manager.models.EmailAddress.send_verification",
    autospec=True,
)
def test_create_duplicate_email(
    mock_send_verification, db, api_client, user, email_address_factory
):
    """
    POST
    email has been used to create EmailAddress (but not verified) by
    another user
    creates new EmailAddress and sends verification email
    """
    email_address_factory(email="newemail@example.com")

    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_201_CREATED

    serializer = EmailAddressSerializer(user.emailaddresses.get())

    assert response.data == serializer.data

    mock_send_verification.assert_called()


@mock.patch(
    "rest_email_manager.models.EmailAddress.send_verification",
    autospec=True,
)
def test_create_already_exists(
    mock_send_verification, db, api_client, user, email_address_factory
):
    """
    POST
    EmailAddress for user and email already exists
    sends another verification email
    """
    email_address_factory(user=user, email="newemail@example.com")

    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_201_CREATED

    mock_send_verification.assert_called()
