import factory

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from faker import Factory as FakerFactory


faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    email = faker.email()
    password = factory.LazyFunction(lambda: make_password("secret"))

    class Meta:
        model = get_user_model()


class EmailAddressFactory(factory.django.DjangoModelFactory):
    """EmailAddress factory."""

    email = faker.email()
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = "rest_email_manager.EmailAddress"


class EmailAddressVerificationFactory(factory.django.DjangoModelFactory):
    """EmailAddressVerification factory."""

    class Meta:
        model = "rest_email_manager.EmailAddressVerification"

    emailaddress = factory.SubFactory(EmailAddressFactory)
