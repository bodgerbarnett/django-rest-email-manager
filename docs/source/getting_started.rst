Getting Started
===============

Available endpoints
-------------------

* ``/emails/``
* ``/emails/verify/``


Requirements
------------

* Python >= 3.6
* Django >= 2.2 and <= 3.1.


Getting the Package
-------------------

The easiest way to install the package is with pip.

To get the most recent release::

   $ pip install django-rest-email-manager


Required Configuration
----------------------

In :file:`settings.py`, make sure the following settings are present::

   INSTALLED_APPS = [
      # At least these default Django apps must be installed:
      'django.contrib.auth',
      'django.contrib.contenttypes',

      # And the app itself
      'rest_email_manager',
   ]


Configure ``urls.py``::

   urlpatterns = [
      ...
      path('email-manager/', include('rest_email_manager.urls')),
      ...
   ]


Post-Installation
-----------------

After the app has been installed and configured, the migrations must be run::

    $ python manage.py migrate
