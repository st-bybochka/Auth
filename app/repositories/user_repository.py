from dataclasses import dataclass
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserProfileSchema
from app.models import UserProfile

@dataclass
class UserRepository:
    session: AsyncSession


    async def get_user_by_username(self, username: str) -> UserProfileSchema | None:
        async with self.session as session:
            result = select(UserProfile).where(UserProfile.username == username)
            user = await session.execute(result)
            return user.scalar_one_or_none()

    async def create_user(self, uasename: str, password: str):
        async with self.session as session:
            user_model = UserProfile(
                username=uasename,
                password=password)
            session.add(user_model)
            await session.commit()

