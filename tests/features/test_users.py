import pytest
from pydantic import ValidationError

from app.features.users.schemas import Address, UserRegistration


def test_public_registration_does_not_accept_a_role() -> None:
    payload = UserRegistration(
        username="library.student",
        full_name="Library Student",
        email="student@example.com",
        phone="+15551234567",
        password="secure-password",
        address=Address(
            line_1="123 Library Street",
            city="Indianapolis",
            state="Indiana",
            postal_code="46204",
            country="United States",
        ),
        college_id="507f1f77bcf86cd799439011",
        library_id="507f1f77bcf86cd799439012",
    )

    assert payload.username == "library.student"


def test_public_registration_rejects_role_selection() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        UserRegistration(
            username="library.student",
            full_name="Library Student",
            email="student@example.com",
            phone="+15551234567",
            password="secure-password",
            address={
                "line_1": "123 Library Street",
                "city": "Indianapolis",
                "state": "Indiana",
                "postal_code": "46204",
                "country": "United States",
            },
            college_id="507f1f77bcf86cd799439011",
            library_id="507f1f77bcf86cd799439012",
            role="SUPER_ADMIN",
        )
