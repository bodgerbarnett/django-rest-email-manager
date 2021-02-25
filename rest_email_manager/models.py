from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

from . import app_settings


User = get_user_model()


def generate_key():
    return get_random_string(64).lower()


class EmailAddress(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(
        User, related_name="emailaddresses", on_delete=models.CASCADE
    )
    verified = models.BooleanField(default=False)

    def send_verification(self):
        verification = self.verifications.create()
        verification.send()


class EmailAddressVerification(models.Model):
    emailaddress = models.ForeignKey(
        EmailAddress, related_name="verifications", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=255, default=generate_key)

    def send(self):
        template_name = "rest_email_manager/emails/verify_email.txt"
        context = {
            "verification_url": app_settings.EMAIL_VERIFICATION_URL.format(
                key=self.key
            )
        }
        message = render_to_string(
            context=context, template_name=template_name
        )
        send_mail(
            "Confirm Email Change",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.emailaddress.email],
        )

    def verify(self):
        if not self.emailaddress.verified:
            self.emailaddress.verified = True
            self.emailaddress.save()
            self.emailaddress.user.email = self.emailaddress.email
            self.emailaddress.user.save()
