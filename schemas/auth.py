from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(LoginRequest):
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    csrf_token: str
    expires_in: int
    role: str
    user: dict


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class MasterVerifyRequest(BaseModel):
    password: str
