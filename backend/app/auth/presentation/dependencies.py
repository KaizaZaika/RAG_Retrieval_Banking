from fastapi import Depends
from app.config import settings
from app.auth.infrastructure.memory_repository import InMemoryUserRepository
from app.auth.infrastructure.password import Argon2PasswordHasher
from app.auth.infrastructure.jwt import PyJWTTokenService
from app.auth.application.use_cases import RegisterUser, LoginUser

# Global instance for the in-memory repository to persist state during application runtime
_in_memory_repo = InMemoryUserRepository()

def get_user_repository() -> InMemoryUserRepository:
    return _in_memory_repo

def get_password_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher()

def get_token_service() -> PyJWTTokenService:
    return PyJWTTokenService(
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.access_token_expire_minutes
    )

def get_register_use_case(
    repo: InMemoryUserRepository = Depends(get_user_repository),
    hasher: Argon2PasswordHasher = Depends(get_password_hasher)
) -> RegisterUser:
    return RegisterUser(user_repository=repo, password_hasher=hasher)

def get_login_use_case(
    repo: InMemoryUserRepository = Depends(get_user_repository),
    hasher: Argon2PasswordHasher = Depends(get_password_hasher),
    token_service: PyJWTTokenService = Depends(get_token_service)
) -> LoginUser:
    return LoginUser(
        user_repository=repo,
        password_hasher=hasher,
        token_service=token_service
    )
