from dataclasses import dataclass
from fastapi import Response, Request
from datetime import datetime, timedelta
from jose import JWTError, jwt

from app.repositories import UserRepository
from app.config import settings
from app.exceptions import UserNotFoundException, UserIncorrectLoginOrPasswordException, TokenMissingException, TokenNotCorrect
from app.services.token_service import TokenService
from app.core import verify_password


@dataclass
class AuthService:
    user_repository: UserRepository
    token_service: TokenService
    settings: settings

    async def login(self, username: str, password: str, response: Response) -> dict:

        user = await self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException

        if not verify_password(password, user.password):
            raise UserIncorrectLoginOrPasswordException

        access_token = await self.token_service.generate_access_token(user.id)
        refresh_token = await self.token_service.generate_refresh_token(user.id)

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def refresh_access_token(self, request: Request, response: Response):

        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise TokenMissingException

        user_id = await self.token_service.is_verify_token(refresh_token)

        access_token = await self.token_service.generate_access_token(user_id)
        response.set_cookie(key="access_token", value=access_token, httponly=True)

        return {"access_token": access_token, "refresh_token": refresh_token}

    async def logout(self, response: Response):

        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")

    async def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (datetime.utcnow() + timedelta(hours=30)).timestamp()
        token = jwt.encode(
            {"user_id": user_id, "exp": expire_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.ALGORITHM
        )
        return token


    async def get_user_id_from_access_token(self, access_token: str) -> int:

        if not access_token:
            raise TokenMissingException

        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ALGORITHM])

        except JWTError:
            raise TokenNotCorrect

        return payload["user_id"]
