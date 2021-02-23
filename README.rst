=============================
django-rest-email-manager
=============================

A Django app to manage user emails.

Documentation
-------------

The full documentation is at https://django-rest-email-manager.readthedocs.io.

Quickstart
----------

Install django-rest-email-manager::

    pip install django-rest-email-manager

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'rest_avatar.apps.DjangoRestAvatarConfig',
        ...
    )

Add django-rest-email-manager's URL patterns:

.. code-block:: python

    from rest_avatar import urls as rest_avatar_urls


    urlpatterns = [
        ...
        path('email-manager/', include('rest_email_manager.urls')),
        ...
    ]

Features
--------

* TODO
