import jwt
from datetime import datetime, timedelta, timezone
from app.auth.domain.services import TokenService

class PyJWTTokenService(TokenService):
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_access_token(self, subject: str) -> str:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=self._expire_minutes)
        
        payload = {
            "sub": subject,
            "iat": now,
            "exp": expires_at
        }
        
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
