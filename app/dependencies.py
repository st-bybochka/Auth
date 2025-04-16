from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository, TaskRepository
from app.database import get_async_session
from app.services import UserService, AuthService, TokenService, TaskService
from app.config import settings
from app.exceptions import TokenNotCorrect, TokenMissingException


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


async def get_task_repository(
        session: AsyncSession = Depends(get_async_session)
) -> TaskRepository:
    return TaskRepository(session)


async def get_task_service(
        task_repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
    )


async def get_request_user_id(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),

) -> int:
    try:

        return await auth_service.get_user_id_from_access_token(request.cookies.get('access_token'))

    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    except TokenMissingException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
