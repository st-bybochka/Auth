import re
from dataclasses import dataclass


from app.repositories import UserRepository
from app.schemas import UserCreateSchema
from app.exceptions import (UserAlreadyRegisteredException, UserIncorrectLenPasswordException, UserNotCapitalLetterException,
                            UserNotSmallLetterException, UserNotDigitException)





@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(self, data: UserCreateSchema):
        if await self.user_repository.get_user_by_username(data.username):
            raise UserAlreadyRegisteredException

        await self.validate_password(data.password)

        await self.user_repository.create_user(data.username, data.password)

    async def validate_password(self, password: str) -> None:
        if len(password) < 8:  # Минимальная длина
            raise UserIncorrectLenPasswordException

        if not re.search(r"[A-Z]", password):  # Хотя бы одна заглавная буква
            raise UserNotCapitalLetterException

        if not re.search(r"[a-z]", password):  # Хотя бы одна строчная буква
            raise UserNotSmallLetterException

        if not re.search(r"[0-9]", password):  # Хотя бы одна цифра
            raise UserNotDigitException


