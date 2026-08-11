from app.shared.infrastructure.database.base import Base
from app.shared.infrastructure.database.engine import engine

# Import every ORM model so SQLAlchemy registers them
from app.shared.infrastructure.database.user import UserModel

Base.metadata.create_all(engine)
