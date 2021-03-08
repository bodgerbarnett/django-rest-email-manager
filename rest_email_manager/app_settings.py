import sys


class AppSettings(object):
    def __init__(self):
        assert self.EMAIL_VERIFICATION_URL

    def _setting(self, name, default):
        """
        Retrieve a setting from the current Django settings.
        Settings are retrieved from the ``REST_EMAIL_MANAGER`` dict in the
        settings file.
        Args:
            name (str):
                The name of the setting to retrieve.
            default:
                The setting's default value.
        Returns:
            The value provided in the settings dictionary if it exists.
            The default value is returned otherwise.
        """
        from django.conf import settings

        settings_dict = getattr(settings, "REST_EMAIL_MANAGER", {})

        return settings_dict.get(name, default)

    @property
    def EMAIL_VERIFICATION_URL(self):
        """
        The template to use for the email verification url.
        """
        return self._setting("EMAIL_VERIFICATION_URL", "")

    @property
    def SEND_VERIFICATION_EMAIL(self):
        """
        The function that sends the verification email
        """
        return self._setting(
            "SEND_VERIFICATION_EMAIL",
            "rest_email_manager.utils.send_verification_email",
        )

    @property
    def SEND_NOTIFICATION_EMAIL(self):
        """
        The function that sends the notification email
        """
        return self._setting(
            "SEND_NOTIFICATION_EMAIL",
            "rest_email_manager.utils.send_notification_email",
        )


app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
