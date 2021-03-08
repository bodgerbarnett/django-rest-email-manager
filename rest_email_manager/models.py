from datetime import timedelta

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.module_loading import import_string

from . import app_settings


User = get_user_model()


def generate_key():
    return get_random_string(64).lower()


class EmailAddress(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(
        User, related_name="emailaddresses", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ["email", "user"]

    def send_verification(self):
        verification = self.verifications.create()
        verification.send()
        verification.send_notification()


class EmailAddressVerification(models.Model):
    emailaddress = models.ForeignKey(
        EmailAddress, related_name="verifications", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=255, default=generate_key)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(days=1)

    def send(self):
        context = {
            "user": self.emailaddress.user,
            "new_email": self.emailaddress.email,
            "verification_url": app_settings.EMAIL_VERIFICATION_URL.format(
                key=self.key
            ),
        }
        to = [self.emailaddress.email]
        import_string(app_settings.SEND_VERIFICATION_EMAIL)(context, to)

    def send_notification(self):
        context = {
            "user": self.emailaddress.user,
            "new_email": self.emailaddress.email,
        }
        to = [self.emailaddress.user.email]
        import_string(app_settings.SEND_NOTIFICATION_EMAIL)(context, to)

    def verify(self):
        self.emailaddress.user.email = self.emailaddress.email
        self.emailaddress.user.save()
