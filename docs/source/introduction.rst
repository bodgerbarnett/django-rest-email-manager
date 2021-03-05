Introduction
============

When users need to update their email on a site built with Django & REST, it is important to ensure that the email they change to is one that they own and have access to before we go ahead and update their email address for them.

If this verification step isn't done, users can lose access to their account.

This application forces users to verify their new email address before it is used for their account.

It does this by sending them an email containing a verification link which, when clicked, will set their user's email address to the new one.

The application will also send an email to the original email address to inform them of the change of address.
