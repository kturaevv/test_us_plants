from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from src.auth import jwt, service, utils
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from src.auth.jwt import parse_jwt_user_data
from src.auth.schemas import AccessTokenResponse, AuthUser, JWTData, UserResponse

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_create),
) -> UserResponse:
    user = await service.create_user(auth_data)
    return UserResponse(**user)


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> UserResponse:
    user = await service.get_user_by_id(jwt_data.user_id)
    return UserResponse(**user)


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(auth_data: AuthUser, response: Response) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
    user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )



""" Api endpoint to test out the security system in swagger UI."""

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/users/tokens_swagger", response_model=AccessTokenResponse)
async def auth_user(auth_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response) -> AccessTokenResponse:
    auth_data.email = auth_data.username
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user["id"])
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )
