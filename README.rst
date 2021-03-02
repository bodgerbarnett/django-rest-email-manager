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
        'rest_email_manager',
        ...
    )

Add django-rest-email-manager's URL patterns:

.. code-block:: python

    urlpatterns = [
        ...
        path('email-manager/', include('rest_email_manager.urls')),
        ...
    ]

Create django-rest-email-manager's database tables:

.. code-block:: python

    python manage.py migrate


Features
--------

* TODO
