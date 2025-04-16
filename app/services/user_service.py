from dataclasses import dataclass

from app.repositories import UserRepository
from app.schemas import UserCreateSchema
from app.exceptions import UserAlreadyRegisteredException


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(self, data: UserCreateSchema):
        if await self.user_repository.get_user_by_username(data.username):
            raise UserAlreadyRegisteredException
        await self.user_repository.create_user(data.username, data.password)
