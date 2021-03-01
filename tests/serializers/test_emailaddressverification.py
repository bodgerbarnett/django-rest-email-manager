from rest_email_manager.serializers import EmailAddressVerificationSerializer


def test_verify(db, api_request, email_address_verification):
    """
    If a valid key, owned by the user is provided, their email should
    be set to the email of the verification
    """
    data = {"key": email_address_verification.key}
    api_request.user = email_address_verification.emailaddress.user
    serializer = EmailAddressVerificationSerializer(
        data=data, context={"request": api_request}
    )
    assert serializer.is_valid()

    serializer.save()

    user = email_address_verification.emailaddress.user
    user.refresh_from_db()
    assert user.email == email_address_verification.emailaddress.email


def test_verify_no_key(db, api_request, email_address_verification):
    """
    If a no key is provided, it should fail
    """
    data = {}
    api_request.user = email_address_verification.emailaddress.user
    serializer = EmailAddressVerificationSerializer(
        data=data, context={"request": api_request}
    )
    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"key"}


def test_verify_wrong_key(db, api_request, email_address_verification):
    """
    If an invalid key is provided, it should fail
    """
    data = {"key": "invalid"}
    api_request.user = email_address_verification.emailaddress.user
    serializer = EmailAddressVerificationSerializer(
        data=data, context={"request": api_request}
    )
    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"key"}


def test_verify_wrong_users_key(
    db, api_request, user_factory, email_address_verification
):
    """
    If the key of another user is provided, it should fail
    """
    data = {"key": email_address_verification.key}
    api_request.user = user_factory()
    serializer = EmailAddressVerificationSerializer(
        data=data, context={"request": api_request}
    )
    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"key"}


def test_verify_email_in_use(
    db, api_request, user_factory, email_address_verification
):
    """
    If an valid key is provided, but the email is already in use it should fail
    """
    user_factory(email=email_address_verification.emailaddress.email)
    data = {"key": email_address_verification.key}
    api_request.user = email_address_verification.emailaddress.user
    serializer = EmailAddressVerificationSerializer(
        data=data, context={"request": api_request}
    )
    assert not serializer.is_valid()
    assert set(serializer.errors.keys()) == {"key"}
