from dataclasses import dataclass
from app.auth.domain.roles import Role
import uuid

@dataclass
class RegisterInput:
    username: str
    email: str
    password: str

@dataclass
class RegisterResult:
    id: uuid.UUID
    username: str
    email: str
    is_active: bool
    role: Role

@dataclass
class LoginInput:
    email: str
    password: str

@dataclass
class TokenResult:
    access_token: str
    token_type: str = "Bearer"
