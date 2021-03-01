from rest_framework import status
from rest_framework.reverse import reverse


def test_verify(db, api_client, email_address_verification):
    """
    POST to verify URL should set the user's email to the EmailAddress' email
    """
    api_client.force_authenticate(
        user=email_address_verification.emailaddress.user
    )
    data = {"key": email_address_verification.key}
    response = api_client.post(reverse("emailaddress-verify"), data)

    user = email_address_verification.emailaddress.user
    user.refresh_from_db()
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert (
        user.email
        == email_address_verification.emailaddress.email
    )


def test_verify_invalid_key(db, api_client, email_address_verification):
    """
    POST to verify URL should fail if given the wrong key
    """
    api_client.force_authenticate(
        user=email_address_verification.emailaddress.user
    )
    data = {"key": "wrong"}
    response = api_client.post(reverse("emailaddress-verify"), data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
