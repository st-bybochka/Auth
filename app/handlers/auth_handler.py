from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.schemas import UserCreateSchema
from app.services import AuthService
from app.dependencies import get_auth_service
from app.exceptions import UserNotFoundException, TokenNotCorrect, UserIncorrectLoginOrPasswordException

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
        data: UserCreateSchema,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> str:

    try:

        return await auth_service.login(data.username, data.password)

    except UserNotFoundException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

    except UserIncorrectLoginOrPasswordException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )

