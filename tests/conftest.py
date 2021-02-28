import pytest

from pytest_factoryboy import register

from rest_framework.test import APIClient, APIRequestFactory

from factories import (
    UserFactory,
    EmailAddressFactory,
    EmailAddressVerificationFactory,
)


@pytest.fixture
def api_request():
    return APIRequestFactory().request()


@pytest.fixture
def api_client():
    return APIClient()


register(UserFactory)
register(EmailAddressFactory)
register(EmailAddressVerificationFactory)
