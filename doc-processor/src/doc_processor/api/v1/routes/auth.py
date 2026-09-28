from fastapi import APIRouter, status

from doc_processor.api.dependencies import AuthServiceDep
from doc_processor.schemas.auth import RegisterRequest, UserResponse

from doc_processor.schemas.auth import (
    RegisterRequest,
    UserResponse,
    LoginRequest,
    TokenResponse,
)

auth_router = APIRouter(prefix="/auth")


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    auth_service: AuthServiceDep,
) -> UserResponse:
    user = await auth_service.register(
        email=str(request.email),
        password=request.password,
    )

    return UserResponse.model_validate(user)

@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginRequest,
    auth_service: AuthServiceDep,
) -> TokenResponse:

    access_token = await auth_service.login(
        email=str(request.email),
        password=request.password,
    )

    return TokenResponse(
        access_token=access_token,
    )