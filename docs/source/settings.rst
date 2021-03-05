Settings
========

You can provide ``REST_EMAIL_MANAGER`` settings like this:

.. code-block:: python

    REST_EMAIL_MANAGER = {
        'EMAIL_VERIFICATION_URL': 'https://example.com/verify/{key}/',
    }


EMAIL_VERIFICATION_URL
----------------------

URL to be sent to the user to verify their new email address. This must contain the ``{key}`` placeholder.
