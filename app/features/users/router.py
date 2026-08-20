from fastapi import APIRouter

from app.core.database import get_database
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserRead, UserRegistration
from app.features.users.service import UserAlreadyExistsError, UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service() -> UserService:
    return UserService(UserRepository(get_database()["users"]))


@router.post("/register", response_model=UserRead, status_code=201)
def register_student(payload: UserRegistration) -> UserRead:
    """Public registration endpoint. It always creates a STUDENT account."""
    try:
        return get_user_service().register_student(payload)
    except UserAlreadyExistsError as error:
        from fastapi import HTTPException

        raise HTTPException(status_code=409, detail=str(error)) from error
