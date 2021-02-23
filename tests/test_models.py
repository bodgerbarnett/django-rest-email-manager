from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

from rest_email_manager.models import EmailAddress, EmailAddressVerification


User = get_user_model()


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@beatles.com", "secret")

    def test_create_emailaddress(self):
        EmailAddress.objects.create(email="ringo@beatles.com", user=self.user)

    def test_create_emailaddressverification(self):
        emailaddress = EmailAddress.objects.create(
            email="ringo@beatles.com", user=self.user
        )
        verification = EmailAddressVerification.objects.create(
            emailaddress=emailaddress
        )

        self.assertTrue(len(verification.key) == 64)

        verification.send()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["ringo@beatles.com"])

        verification_url = "https://example.com/verify/{key}".format(
            key=verification.key
        )

        self.assertIn(verification_url, mail.outbox[0].body)

    def tearDown(self):
        pass
