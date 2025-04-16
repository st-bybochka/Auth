
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.exceptions import UserAlreadyRegisteredException
from app.services import UserService
from app.dependencies import get_user_service
from app.schemas import UserCreateSchema


router = APIRouter(
    prefix="/user",
    tags=["User"],

)


@router.post("/create/user")
async def create_user(
        data: UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        await user_service.create_user(data)
    except UserAlreadyRegisteredException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )