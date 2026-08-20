from fastapi import APIRouter

from app.features.auth.router import router as auth_router
from app.features.books.router import router as books_router
from app.features.categories.router import router as categories_router
from app.features.circulation.router import router as circulation_router
from app.features.colleges.router import router as colleges_router
from app.features.dashboard.router import router as dashboard_router
from app.features.libraries.router import router as libraries_router
from app.features.requests.router import router as requests_router
from app.features.students.router import router as students_router
from app.features.users.router import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(colleges_router)
api_router.include_router(libraries_router)
api_router.include_router(categories_router)
api_router.include_router(books_router)
api_router.include_router(students_router)
api_router.include_router(requests_router)
api_router.include_router(circulation_router)
api_router.include_router(dashboard_router)
