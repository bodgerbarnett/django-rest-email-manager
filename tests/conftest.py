from pytest_factoryboy import register

from factories import (
    UserFactory,
    EmailAddressFactory,
    EmailAddressVerificationFactory,
)


register(UserFactory)
register(EmailAddressFactory)
register(EmailAddressVerificationFactory)
