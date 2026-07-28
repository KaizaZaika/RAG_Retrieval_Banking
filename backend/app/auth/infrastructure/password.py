from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from app.auth.domain.services import PasswordHasher

class Argon2PasswordHasher(PasswordHasher):
    def __init__(self):
        self._pwd_context = PasswordHash((Argon2Hasher(),))

    def hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
