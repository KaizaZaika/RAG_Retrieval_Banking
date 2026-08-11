from app.auth.domain.entities import User
from app.auth.domain.exceptions import UserAlreadyExistsError, InvalidCredentialsError, InactiveUserError
from app.auth.domain.repositories import UserRepository
from app.auth.domain.services import PasswordHasher, TokenService
from .models import RegisterInput, RegisterResult, LoginInput, TokenResult

class RegisterUser:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def registerForUser(self, input_data: RegisterInput) -> RegisterResult:
        if self._user_repository.get_by_email(input_data.email):
            raise UserAlreadyExistsError("Email is already registered.")
            
        if self._user_repository.get_by_username(input_data.username):
            raise UserAlreadyExistsError("Username is already taken.")

        hashed_password_user = self._password_hasher.hash(input_data.password)
        
        user = User(
            username=input_data.username,
            email=input_data.email,
            password_hash=hashed_password_user
        )
        
        self._user_repository.add(user)
        
        return RegisterResult(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role=user.role
        )

class LoginUser:
    def __init__(
        self, 
        user_repository: UserRepository, 
        password_hasher: PasswordHasher, 
        token_service: TokenService
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def logInUser(self, input_data: LoginInput) -> TokenResult:
        user = self._user_repository.get_by_email(input_data.email)
        
        if not user:
            raise InvalidCredentialsError("Invalid email or password.")
            
        if not self._password_hasher.verify(input_data.password, user.password_hash):
            raise InvalidCredentialsError("Invalid email or password.")
            
        if not user.is_active:
            raise InactiveUserError("User account is inactive.")

        token = self._token_service.create_access_token(str(user.id))
        
        return TokenResult(access_token=token)
class GetCurrentUser:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def get_user(self, user_id: uuid.UUID) -> RegisterResult:
        user = self._user_repository.get_by_id(user_id)

        if user is None:
            raise InvalidCredentialsError("User no longer exists.")

        return RegisterResult(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role=user.role,
        )
