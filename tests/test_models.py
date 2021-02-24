from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail

from model_bakery import baker


User = get_user_model()


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("john@beatles.com", "secret")

    def test_create_emailaddress(self):
        emailaddress = baker.make(
            "EmailAddress", email="ringo@beatles.com", user=self.user
        )

        self.assertFalse(emailaddress.verified)

    def test_create_emailaddressverification(self):
        emailaddress = baker.make(
            "EmailAddress", email="ringo@beatles.com", user=self.user
        )
        verification = baker.make(
            "EmailAddressVerification", emailaddress=emailaddress
        )

        self.assertTrue(len(verification.key) == 64)

        verification.send()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["ringo@beatles.com"])

        verification_url = "https://example.com/verify/{key}".format(
            key=verification.key
        )

        self.assertIn(verification_url, mail.outbox[0].body)

    def test_send_emailaddress_verification(self):
        emailaddress = baker.make(
            "EmailAddress", email="ringo@beatles.com", user=self.user
        )
        emailaddress.send_verification()
        self.assertEqual(emailaddress.verifications.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_verify_emailaddress(self):
        emailaddress = baker.make(
            "EmailAddress", email="ringo@beatles.com", user=self.user
        )
        verification = baker.make(
            "EmailAddressVerification", emailaddress=emailaddress
        )
        verification.verify()
        self.assertTrue(emailaddress.verified)

    def tearDown(self):
        pass
