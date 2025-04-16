from dataclasses import dataclass
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenNotCorrect

@dataclass
class TokenService:
    settings: settings

    async def generate_access_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        token = jwt.encode(
            {"user_id": user_id, "exp": expire},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        return token

    async def generate_refresh_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        token = jwt.encode(
            {"user_id": user_id, "exp": expire},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        return token

    async def is_verify_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload["user_id"]
        except JWTError:
            raise TokenNotCorrect



