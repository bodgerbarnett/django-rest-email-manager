from django.core import mail

from rest_email_manager.models import EmailAddressVerification


def test_emailaddressverification(db, email_address_verification):
    assert isinstance(email_address_verification, EmailAddressVerification)


def test_emailaddressverification_key(db, email_address_verification):
    assert len(email_address_verification.key) == 64


def test_emailaddressverification_send(db, email_address_verification):
    email_address_verification.send()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [email_address_verification.emailaddress.email]

    verification_url = "https://example.com/verify/{key}".format(
        key=email_address_verification.key
    )

    assert verification_url in mail.outbox[0].body


def test_emailaddressverification_send_notification(
    db, email_address_verification
):
    email_address_verification.send_notification()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [
        email_address_verification.emailaddress.user.email
    ]

    assert (
        email_address_verification.emailaddress.user.email
        in mail.outbox[0].body
    )
    assert email_address_verification.emailaddress.email in mail.outbox[0].body


def test_emailaddressverification_verify(db, email_address_verification):
    email_address_verification.verify()
    assert (
        email_address_verification.emailaddress.user.email
        == email_address_verification.emailaddress.email
    )
