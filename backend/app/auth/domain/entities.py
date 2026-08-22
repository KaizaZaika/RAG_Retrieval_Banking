import uuid
from dataclasses import dataclass, field
from .roles import Role
@dataclass
class User:
    username: str
    email: str
    password_hash: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
    role: Role = Role.STAFF
