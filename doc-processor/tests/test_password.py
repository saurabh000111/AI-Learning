from doc_processor.core.security import (
    hash_password,
    verify_password,
)


def test_password_hash_and_verify_round_trip() -> None:
    password = "TestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False
