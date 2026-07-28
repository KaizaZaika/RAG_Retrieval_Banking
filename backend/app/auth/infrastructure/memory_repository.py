from typing import Optional, List
from app.auth.domain.entities import User
from app.auth.domain.repositories import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: List[User] = []

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users:
            if user.email == email:
                return user
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users:
            if user.username == username:
                return user
        return None

    def add(self, user: User) -> None:
        self._users.append(user)
        
    def clear(self) -> None:
        """Utility method to reset the repository state between tests."""
        self._users.clear()
