from fastapi import APIRouter, Depends, HTTPException, Response, Request
from typing import Annotated

from app.schemas import UserCreateSchema
from app.services import AuthService, auth_service
from app.dependencies import get_auth_service
from app.exceptions import UserNotFoundException, UserIncorrectLoginOrPasswordException, UserBlockedException

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
        data: UserCreateSchema,
        response: Response,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> dict:
    try:

        return await auth_service.login(data.username, data.password, response)

    except (UserNotFoundException, UserIncorrectLoginOrPasswordException, UserBlockedException) as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )


@router.post("/logout")
async def logout(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response):
    try:
        await auth_service.logout(response)
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )


@router.get("/refresh")
async def refresh(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response,
        request: Request,
):
    try:
        return await auth_service.refresh_access_token(request, response)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
