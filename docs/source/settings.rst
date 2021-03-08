Settings
========

You can provide ``REST_EMAIL_MANAGER`` settings like this:

.. code-block:: python

    REST_EMAIL_MANAGER = {
        'EMAIL_VERIFICATION_URL': 'https://example.com/verify/{key}/',
        'SEND_VERIFICATION_EMAIL': 'rest_email_manager.utils.send_verification_email',
        'SEND_NOTIFICATION_EMAIL': 'rest_email_manager.utils.send_notification_email'
    }


EMAIL_VERIFICATION_URL
----------------------

URL to be sent to the user to verify their new email address. This must contain the ``{key}`` placeholder.

SEND_VERIFICATION_EMAIL
-----------------------

Path to the function that is called to send the verification email to the new email address of the user.

SEND_NOTIFICATION_EMAIL
-----------------------

Path to the function that is called to send the notification email to the current email address of the user.
