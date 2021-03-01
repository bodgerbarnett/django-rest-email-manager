from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_manager.serializers import EmailAddressSerializer


def test_get(db, api_client, email_address):
    """
    GET
    returns email address details
    """
    api_client.force_authenticate(user=email_address.user)
    response = api_client.get(
        reverse("emailaddress-detail", args=[email_address.id])
    )

    assert response.status_code == status.HTTP_200_OK

    serializer = EmailAddressSerializer(email_address)

    assert response.data == serializer.data


def test_get_no_auth(api_client):
    """
    GET
    no authentication
    fails permission denied
    """
    response = api_client.get(reverse("emailaddress-detail", kwargs={"pk": 1}))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_other_users_email(db, api_client, email_address_factory, user):
    """
    GET
    attempt to get another user's EmailAddress
    fails with 404
    """
    email_address = email_address_factory()
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse("emailaddress-detail", kwargs={"pk": email_address.id})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_non_existent(db, api_client, user):
    """
    GET
    attempt to get a non-existent EmailAddress
    fails with 404
    """
    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse("emailaddress-detail", kwargs={"pk": 444})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put(db, api_client, email_address):
    """
    PUT
    not allowed
    """
    api_client.force_authenticate(user=email_address.user)
    data = {"email": "another@example.com", "current_password": "secret"}
    response = api_client.put(
        reverse("emailaddress-detail", kwargs={"pk": email_address.id}),
        data
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patch(db, api_client, email_address):
    """
    PATCH
    not allowed
    """
    api_client.force_authenticate(user=email_address.user)
    data = {"email": "another@example.com"}
    response = api_client.patch(
        reverse("emailaddress-detail", kwargs={"pk": email_address.id}),
        data
    )
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_delete(db, api_client, email_address):
    """
    DELETE
    delete EmailAddress
    succeeds
    """
    api_client.force_authenticate(user=email_address.user)

    response = api_client.delete(
        reverse("emailaddress-detail", kwargs={"pk": email_address.id})
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_no_auth(db, api_client, email_address):
    """
    DELETE
    no authentication
    fails permission denied
    """
    response = api_client.delete(
        reverse("emailaddress-detail", kwargs={"pk": email_address.id})
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_other_users_email(db, api_client, user, email_address_factory):
    """
    DELETE
    delete EmailAddress owned by someone else
    fails permission denied
    """
    email_address = email_address_factory()
    api_client.force_authenticate(user=user)

    response = api_client.delete(
        reverse("emailaddress-detail", kwargs={"pk": email_address.id})
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
