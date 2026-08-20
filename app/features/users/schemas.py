"""User schemas and the four-role organizational-scope contract."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserRole(StrEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    COLLEGE_ADMIN = "COLLEGE_ADMIN"
    LIBRARY_ADMIN = "LIBRARY_ADMIN"
    STUDENT = "STUDENT"


class Address(BaseModel):
    line_1: str = Field(min_length=2, max_length=150)
    line_2: str | None = Field(default=None, max_length=150)
    city: str = Field(min_length=2, max_length=80)
    state: str = Field(min_length=2, max_length=80)
    postal_code: str = Field(min_length=3, max_length=20)
    country: str = Field(min_length=2, max_length=80)


class UserRegistration(BaseModel):
    """Public registration payload. It always results in a STUDENT account."""

    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[1-9]\d{7,14}$")
    password: str = Field(min_length=8, max_length=128)
    address: Address
    college_id: str = Field(min_length=1)
    library_id: str = Field(min_length=1)


class UserCreate(BaseModel):
    """Internal user-creation payload for authorized administrator workflows."""

    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[1-9]\d{7,14}$")
    password: str = Field(min_length=8, max_length=128)
    address: Address
    role: UserRole
    college_id: str | None = None
    library_id: str | None = None

    @model_validator(mode="after")
    def validate_organizational_scope(self) -> "UserCreate":
        if self.role is UserRole.SUPER_ADMIN:
            if self.college_id is not None or self.library_id is not None:
                raise ValueError("SUPER_ADMIN must not have college_id or library_id")
        elif self.role is UserRole.COLLEGE_ADMIN:
            if self.college_id is None or self.library_id is not None:
                raise ValueError("COLLEGE_ADMIN requires college_id and must not have library_id")
        elif self.college_id is None or self.library_id is None:
            raise ValueError(f"{self.role} requires both college_id and library_id")
        return self


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    full_name: str
    email: EmailStr
    phone: str
    address: Address
    role: UserRole
    college_id: str | None
    library_id: str | None
    is_active: bool
    created_at: str
    updated_at: str
