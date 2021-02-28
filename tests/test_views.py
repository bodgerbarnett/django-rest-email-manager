from rest_framework import status
from rest_framework.reverse import reverse

from rest_email_manager.serializers import EmailAddressSerializer


def test_create_emailaddress(db, api_client, user):
    api_client.force_authenticate(user=user)

    data = {"email": "newemail@example.com", "current_password": "secret"}

    response = api_client.post(reverse("emailaddress-list"), data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = EmailAddressSerializer(user.emailaddresses.get())

    assert response.data == serializer.data
