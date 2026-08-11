import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from sqlalchemy.orm import Session

from app.auth.application.use_cases import (
    GetCurrentUser,
    LoginUser,
    RegisterUser,
)
from app.auth.domain.exceptions import InvalidCredentialsError
from app.auth.domain.repositories import UserRepository
from app.auth.infrastructure.jwt import PyJWTTokenService
from app.auth.infrastructure.password import Argon2PasswordHasher
from app.auth.infrastructure.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from app.config import settings
from app.shared.infrastructure.database.session import get_db



bearer_scheme = HTTPBearer()

def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return SqlAlchemyUserRepository(db)


def get_password_hasher() -> Argon2PasswordHasher:
    return Argon2PasswordHasher()


def get_token_service() -> PyJWTTokenService:
    return PyJWTTokenService(
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.access_token_expire_minutes,
    )


def get_register_use_case(
    repo: UserRepository = Depends(get_user_repository),
    hasher: Argon2PasswordHasher = Depends(get_password_hasher),
) -> RegisterUser:
    return RegisterUser(
        user_repository=repo,
        password_hasher=hasher,
    )


def get_login_use_case(
    repo: UserRepository = Depends(get_user_repository),
    hasher: Argon2PasswordHasher = Depends(get_password_hasher),
    token_service: PyJWTTokenService = Depends(get_token_service),
) -> LoginUser:
    return LoginUser(
        user_repository=repo,
        password_hasher=hasher,
        token_service=token_service,
    )


def get_current_user_use_case(
    repo: UserRepository = Depends(get_user_repository),
) -> GetCurrentUser:
    return GetCurrentUser(user_repository=repo)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token_service: PyJWTTokenService = Depends(get_token_service),
    use_case: GetCurrentUser = Depends(get_current_user_use_case),
):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        subject = token_service.decode_access_token(token)
        user_id = uuid.UUID(subject)

        return use_case.get_user(user_id)

    except (ValueError, InvalidCredentialsError) as exc:
        raise credentials_error from exc
