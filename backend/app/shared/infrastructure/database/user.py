import uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy import Boolean, String, true
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.auth.domain.roles import Role
from app.shared.infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(320),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=true(),
        nullable=False,
    )
    role: Mapped[Role] = mapped_column(
    SAEnum(
        Role,
        name="user_role",
        values_callable=lambda enum_cls: [
            member.value for member in enum_cls
            ],
        ),
        nullable=False,
        default=Role.STAFF,
        server_default=Role.STAFF.value,
    )
    
