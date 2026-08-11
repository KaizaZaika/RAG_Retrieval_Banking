from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.domain.entities import User
from app.auth.domain.repositories import UserRepository
from app.shared.infrastructure.database.user import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session
    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        model = self._session.get(UserModel, user_id)

        if model is None:
            return None

        return self._to_domain(model)
    def get_by_email(self, email: str) -> User | None:
        statement = select(UserModel).where(
            UserModel.email == email
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_username(self, username: str) -> User | None:
        statement = select(UserModel).where(
            UserModel.username == username
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def add(self, user: User) -> None:
        model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            is_active=user.is_active,
            role=user.role,
        )

        self._session.add(model)

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            is_active=model.is_active,
            role=model.role,
        )
