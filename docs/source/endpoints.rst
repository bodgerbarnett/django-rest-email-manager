Endpoints
=========

Email Addresses
---------------

Use this endpoint to list/create the authenticated user's email addresses.

**Default URL**: ``/emails/``

+----------+--------------------------------+----------------------------------+
| Method   |           Request              |           Response               |
+==========+================================+==================================+
| ``GET``  |    --                          | ``HTTP_200_OK``                  |
|          |                                |                                  |
|          |                                | * ``email``                      |
+----------+--------------------------------+----------------------------------+
| ``POST`` | ``email``                      | ``HTTP_200_OK``                  |
|          | ``current_password``           |                                  |
|          |                                | * ``email``                      |
|          |                                |                                  |
|          |                                | ``HTTP_400_BAD_REQUEST``         |
|          |                                |                                  |
|          |                                | * ``current_password``           |
+----------+--------------------------------+----------------------------------+


Email Address Delete
--------------------

Use this endpoint to delete an email address for the authenticated user.

**Default URL**: ``/emails/``

+------------+---------------------------------+----------------------------------+
| Method     |  Request                        | Response                         |
+============+=================================+==================================+
| ``DELETE`` | * ``current_password``          | ``HTTP_204_NO_CONTENT``          |
|            |                                 |                                  |
|            |                                 | ``HTTP_400_BAD_REQUEST``         |
|            |                                 |                                  |
|            |                                 | * ``current_password``           |
+------------+---------------------------------+----------------------------------+


Email Address Verify
--------------------

Use this endpoint to verify an email address for the authenticated user.

**Default URL**: ``/emails/verify/``

+------------+---------------------------------+----------------------------------+
| Method     |  Request                        | Response                         |
+============+=================================+==================================+
| ``POST``   | * ``key``                       | ``HTTP_204_NO_CONTENT``          |
|            |                                 |                                  |
|            |                                 | ``HTTP_400_BAD_REQUEST``         |
|            |                                 |                                  |
|            |                                 | * ``key``                        |
+------------+---------------------------------+----------------------------------+
