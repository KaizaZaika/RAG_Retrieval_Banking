from typing import Protocol, Optional
from .entities import User

class UserRepository(Protocol):
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    def get_by_username(self, username: str) -> Optional[User]:
        ...

    def add(self, user: User) -> None:
        ...
