from unittest import mock

from rest_framework import status
from rest_framework.reverse import reverse


def test_verify(db, api_client, email_address_verification):
    """
    set the user's email to the EmailAddress' email
    """
    api_client.force_authenticate(
        user=email_address_verification.emailaddress.user
    )
    data = {"key": email_address_verification.key}
    response = api_client.post(reverse("emailaddress-verify"), data)

    user = email_address_verification.emailaddress.user
    user.refresh_from_db()
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.email == email_address_verification.emailaddress.email


def test_verify_no_auth(db, api_client, email_address_verification):
    """
    fail without auth
    """
    data = {"key": email_address_verification.key}
    response = api_client.post(reverse("emailaddress-verify"), data)

    user = email_address_verification.emailaddress.user
    user.refresh_from_db()
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_verify_invalid_key(db, api_client, email_address_verification):
    """
    fail if given the wrong key
    """
    api_client.force_authenticate(
        user=email_address_verification.emailaddress.user
    )
    data = {"key": "wrong"}
    response = api_client.post(reverse("emailaddress-verify"), data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_verify_email_taken(
    db, api_client, user_factory, email_address_verification
):
    """
    fail if the verification's email address has already been taken by
    another user
    """
    user_factory(email=email_address_verification.emailaddress.email)
    api_client.force_authenticate(
        user=email_address_verification.emailaddress.user
    )
    data = {"key": email_address_verification.key}
    response = api_client.post(reverse("emailaddress-verify"), data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_verify_expired(db, api_client, email_address_verification):
    """
    fail if verification has expired
    """
    api_client.force_authenticate(
        user=email_address_verification.emailaddress.user
    )
    data = {"key": email_address_verification.key}

    with mock.patch(
        "rest_email_manager.models.EmailAddressVerification.is_expired",
        new_callable=mock.PropertyMock,
    ) as mock_is_expired:
        mock_is_expired.return_value = True

        response = api_client.post(reverse("emailaddress-verify"), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
