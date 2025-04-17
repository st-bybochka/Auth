from dataclasses import dataclass
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserProfileSchema
from app.models import UserProfile
from app.core import hash_password
from app.services.token_service import TokenService


@dataclass
class UserRepository:
    session: AsyncSession
    token_service: TokenService

    async def get_user_by_username(self, username: str) -> UserProfileSchema | None:
        async with self.session as session:
            result = select(UserProfile).where(UserProfile.username == username)
            user = await session.execute(result)
            return user.scalar_one_or_none()

    async def create_user(self, username: str, password: str):
        async with self.session as session:
            user_model = UserProfile(
                username=username,
                password=hash_password(password),
                login_attempts=0,
                block_until=None
            )
            session.add(user_model)
            await session.commit()

    async def update_user(self, user: UserProfile):
        async with self.session as session:
            session.add(user)
            await self.session.commit()

