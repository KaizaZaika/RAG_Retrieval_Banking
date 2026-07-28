from pydantic import BaseModel, EmailStr, Field
import uuid

class RegisterRequestSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserResponseSchema(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool

class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str

class ErrorResponseSchema(BaseModel):
    detail: str
