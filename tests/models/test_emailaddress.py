from unittest import mock

from rest_email_manager.models import EmailAddress


def test_emailaddress(db, email_address):
    assert isinstance(email_address, EmailAddress)


@mock.patch(
    "rest_email_manager.models.EmailAddressVerification.send",
    autospec=True,
)
@mock.patch(
    "rest_email_manager.models.EmailAddressVerification.send_notification",
    autospec=True,
)
def test_emailaddress_send_verification(
    mock_send, mock_send_notification, db, email_address
):
    email_address.send_verification()
    assert email_address.verifications.count() == 1
    mock_send.assert_called()
    mock_send_notification.assert_called()
