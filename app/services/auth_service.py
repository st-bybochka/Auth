from dataclasses import dataclass

from app.repositories import UserRepository
from app.config import settings
from app.exceptions import UserNotFoundException, UserIncorrectLoginOrPasswordException
from app.services.token_service import TokenService
from app.schemas import UserProfileSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    token_service: TokenService
    settings: settings

    async def login(self, username: str, password: str) -> str:

        user = await self.user_repository.get_user_by_username(username)
        await self.is_validate_user(user, password)

        access_token = await self.token_service.generate_access_token(user.id)
        await self.token_service.is_verify_token(access_token)

        return access_token

    async def is_validate_user(self, user: UserProfileSchema, password: str):
        if not user:
            raise UserNotFoundException

        if password != user.password:
            raise UserIncorrectLoginOrPasswordException
