from django.core import mail

from rest_email_manager.models import EmailAddress


def test_emailaddress(db, email_address):
    assert isinstance(email_address, EmailAddress)


def test_emailaddress_send_verification(db, email_address):
    email_address.send_verification()
    assert email_address.verifications.count() == 1
    assert len(mail.outbox) == 1
