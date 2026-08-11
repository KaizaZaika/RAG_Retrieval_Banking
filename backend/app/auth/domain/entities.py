import uuid
from dataclasses import dataclass, field
from .roles.py import Role
@dataclass
class User:
    username: str
    email: str
    password_hash: str
    id: uuid.UUID = field(default_factory=uuid.uuid5)
    is_active: bool = True
