from copy import deepcopy

import pytest
from pydantic import ValidationError

from app.core.security import verify_password
from app.features.users.schemas import Address, UserCreate, UserRole
from app.features.users.service import UserAlreadyExistsError, UserService

COLLEGE_ID = "507f1f77bcf86cd799439011"
LIBRARY_ID = "507f1f77bcf86cd799439012"
PROFILE_FIELDS = {
    "username": "ada.lovelace",
    "phone": "+15551234567",
    "address": Address(
        line_1="123 Library Street",
        city="Indianapolis",
        state="Indiana",
        postal_code="46204",
        country="United States",
    ),
}


class FakeUserRepository:
    def __init__(self) -> None:
        self.documents: list[dict] = []

    def find_by_email(self, email: str) -> dict | None:
        return next((document for document in self.documents if document["email"] == email), None)

    def find_by_username(self, username: str) -> dict | None:
        return next((document for document in self.documents if document["username"] == username), None)

    def create(self, document: dict) -> dict:
        stored = deepcopy(document)
        stored["_id"] = "507f1f77bcf86cd799439013"
        for field in ("college_id", "library_id"):
            if stored[field] is not None:
                stored[field] = str(stored[field])
        for field in ("created_at", "updated_at"):
            stored[field] = stored[field].isoformat()
        stored["id"] = stored.pop("_id")
        self.documents.append(stored)
        return stored


def test_student_user_is_scoped_and_password_is_hashed() -> None:
    repository = FakeUserRepository()
    service = UserService(repository)

    user = service.create_user(
        UserCreate(
            **PROFILE_FIELDS,
            full_name="Ada Lovelace",
            email="ADA@EXAMPLE.COM",
            password="a-secure-password",
            role=UserRole.STUDENT,
            college_id=COLLEGE_ID,
            library_id=LIBRARY_ID,
        )
    )

    assert user.email == "ada@example.com"
    assert user.role is UserRole.STUDENT
    assert verify_password("a-secure-password", repository.documents[0]["password_hash"])
    assert "password" not in user.model_dump()


def test_college_admin_cannot_be_assigned_a_library() -> None:
    with pytest.raises(ValidationError, match="must not have library_id"):
        UserCreate(
            **PROFILE_FIELDS,
            full_name="College Admin",
            email="admin@example.com",
            password="a-secure-password",
            role=UserRole.COLLEGE_ADMIN,
            college_id=COLLEGE_ID,
            library_id=LIBRARY_ID,
        )


def test_duplicate_email_is_rejected() -> None:
    repository = FakeUserRepository()
    service = UserService(repository)
    payload = UserCreate(
        **PROFILE_FIELDS,
        full_name="Platform Admin",
        email="admin@example.com",
        password="a-secure-password",
        role=UserRole.SUPER_ADMIN,
    )

    service.create_user(payload)

    with pytest.raises(UserAlreadyExistsError):
        service.create_user(payload)
