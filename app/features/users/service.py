"""User-management use cases independent of FastAPI request handling."""

from datetime import UTC, datetime
from typing import Protocol

from bson import ObjectId

from app.core.security import hash_password
from app.features.users.schemas import UserCreate, UserRead, UserRegistration, UserRole


class UserRepositoryProtocol(Protocol):
    def find_by_email(self, email: str) -> dict | None: ...

    def find_by_username(self, username: str) -> dict | None: ...

    def create(self, document: dict) -> dict: ...


class UserAlreadyExistsError(Exception):
    """Raised when a user email is already registered."""


class UserService:
    def __init__(self, repository: UserRepositoryProtocol):
        self._repository = repository

    def create_user(self, payload: UserCreate) -> UserRead:
        email = str(payload.email).lower()
        if self._repository.find_by_email(email):
            raise UserAlreadyExistsError("A user with this email already exists")
        username = payload.username.lower()
        if self._repository.find_by_username(username):
            raise UserAlreadyExistsError("This username is already in use")

        now = datetime.now(UTC)
        document = {
            "username": username,
            "full_name": payload.full_name.strip(),
            "email": email,
            "phone": payload.phone,
            "address": payload.address.model_dump(),
            "password_hash": hash_password(payload.password),
            "role": payload.role.value,
            "college_id": self._to_object_id(payload.college_id),
            "library_id": self._to_object_id(payload.library_id),
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        return UserRead.model_validate(self._repository.create(document))

    def register_student(self, payload: UserRegistration) -> UserRead:
        """Create a student account; public callers cannot assign an admin role."""
        return self.create_user(
            UserCreate(
                **payload.model_dump(),
                role=UserRole.STUDENT,
            )
        )

    @staticmethod
    def _to_object_id(value: str | None) -> ObjectId | None:
        if value is None:
            return None
        if not ObjectId.is_valid(value):
            raise ValueError("college_id and library_id must be valid MongoDB ObjectIds")
        return ObjectId(value)
