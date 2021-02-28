from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_manager.serializers import EmailAddressSerializer


list_url = reverse("emailaddress-list")


# 1. list (GET)
#   - returns all user's EmailAddresses
#   - fails if not authenticated
def test_list_emailaddresses(db, api_client, user, email_address_factory):
    """
    list view returns all user's email addresses
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


def test_list_emailaddresses_no_auth(db, api_client):
    """
    list view requires authentication
    """
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


# 2. retrieve (GET)
#   - TODO returns EmailAddress if exists and owned by user
#   - TODO fails if not authenticated
#   - TODO fails if doesn't exist
#   - TODO fails if doesn't belong to user

# 3. create (POST)
#   - returns new EmailAddress if valid email and password
#   - sends a new verification if valid but EmailAddress already exists
#   - fails if not authenticated
#   - fails if no email
#   - fails if no password
#   - fails if wrong password
#   - fails if another user already has that email
def test_create_emailaddress(db, api_client, user):
    """
    POST to list view creates new EmailAddress
    """
    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_201_CREATED

    serializer = EmailAddressSerializer(user.emailaddresses.get())

    assert response.data == serializer.data


def test_create_emailaddress_no_auth(db, api_client):
    """
    POST to list view requires authentication
    """
    data = {"email": "newemail@example.com", "current_password": "secret"}
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_emailaddress_no_email(db, api_client, user):
    """
    POST to list view requires email address
    """
    data = {"current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_emailaddress_no_password(db, api_client, user):
    """
    POST to list view requires password
    """
    data = {"email": "newemail@example.com"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_emailaddress_wrong_password(db, api_client, user):
    """
    POST to list view fails if password is wrong
    """
    data = {"email": "newemail@example.com", "current_password": "wrong"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_emailaddress_duplicate_user_email(
    db, api_client, user, user_factory
):
    """
    POST to list view fails if email is already set on another user
    """
    user_factory(email="newemail@example.com")

    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_emailaddress_already_exists(
    db, api_client, user, email_address_factory
):
    """
    POST to list view sends another verification email if email already exists
    """
    email_address_factory(user=user, email="newemail@example.com")

    data = {"email": "newemail@example.com", "current_password": "secret"}

    api_client.force_authenticate(user=user)
    response = api_client.post(list_url, data)
    assert response.status_code == status.HTTP_201_CREATED


# 4. update (PUT)
# TODO THINK ABOUT DISABLING THIS
#   - returns updated EmailAddress and sends verification email if valid email
#   - fails if not authenticated
#   - fails if no email
#   - fails if another user already has that email
#   - fails if new email is that of another EmailAddress

# 5. partial update (PATCH)
# TODO THINK ABOUT DISABLING THIS
#   - fails if not authenticated
#   - fails if another user already has that email

# 6. destroy (DELETE)
#   - TODO fails if not authenticated
#   - TODO fails if it's not owned by the user
