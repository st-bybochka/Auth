from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository
from app.database import get_async_session
from app.services import UserService, AuthService, TokenService
from app.config import settings


async def get_token_service() -> TokenService:
    return TokenService(settings=settings)


async def get_user_repository(
        session: AsyncSession = Depends(get_async_session),
        token_service: TokenService = Depends(get_token_service),
) -> UserRepository:
    return UserRepository(
        session=session,
        token_service=token_service
    )


async def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository=user_repository)


async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        token_service: TokenService = Depends(get_token_service)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        token_service=token_service,
        settings=settings
    )
