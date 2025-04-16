from dataclasses import dataclass
from fastapi import Response, Request

from app.repositories import UserRepository
from app.config import settings
from app.exceptions import UserNotFoundException, UserIncorrectLoginOrPasswordException, TokenMissingException
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
