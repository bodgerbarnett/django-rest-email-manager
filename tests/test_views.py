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
    email_address_factory(user=user)
    email_address_factory(user=user)

    # create an email address for another user
    email_address_factory()

    serializer = EmailAddressSerializer(
        user.emailaddresses.all(), many=True
    )

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
#   - TODO sends a new verification if valid email and password but EmailAddress already exists
#   - TODO fails if not authenticated
#   - TODO fails if no email
#   - TODO fails if no password
#   - TODO fails if wrong password
#   - TODO fails if another user already has that email
def test_create_emailaddress(db, api_client, user):
    """
    POST to list view creates new EmailAddress and sends verification email
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
