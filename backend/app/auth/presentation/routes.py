from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.application.use_cases import RegisterUser, LoginUser
from app.auth.application.models import RegisterInput, LoginInput
from app.auth.domain.exceptions import UserAlreadyExistsError, InvalidCredentialsError, InactiveUserError
from .schemas import (
    RegisterRequestSchema,
    UserResponseSchema,
    LoginRequestSchema,
    TokenResponseSchema,
    ErrorResponseSchema
)
from .dependencies import get_register_use_case, get_login_use_case, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register", 
    response_model=UserResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": ErrorResponseSchema}}
)
def register(
    payload: RegisterRequestSchema,
    use_case: RegisterUser = Depends(get_register_use_case)
):
    try:
        input_data = RegisterInput(
            username=payload.username,
            email=payload.email,
            password=payload.password
        )
        result = use_case.registerForUser(input_data)
        
        return UserResponseSchema(
            id=result.id,
            username=result.username,
            email=result.email,
            is_active=result.is_active,
            role=result.role,
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.post(
    "/login", 
    response_model=TokenResponseSchema,
    responses={
        401: {"model": ErrorResponseSchema},
        403: {"model": ErrorResponseSchema}
    }
)
def login(
    payload: LoginRequestSchema,
    use_case: LoginUser = Depends(get_login_use_case)
):
    try:
        input_data = LoginInput(
            email=payload.email,
            password=payload.password
        )
        result = use_case.logInUser(input_data)
        
        return TokenResponseSchema(
            access_token=result.access_token,
            token_type=result.token_type
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except InactiveUserError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
@router.get(
    "/me",
    response_model=UserResponseSchema,
)
def me(
    current_user=Depends(get_current_user),
):
    return UserResponseSchema(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        role=current_user.role,
    )
