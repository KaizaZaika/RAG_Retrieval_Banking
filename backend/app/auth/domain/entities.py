import uuid
from dataclasses import dataclass, field

@dataclass
class User:
    username: str
    email: str
    password_hash: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
