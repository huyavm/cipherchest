from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from schemas.auth import LoginRequest, RegisterRequest, RefreshRequest, LogoutRequest, TokenResponse, MasterVerifyRequest
from schemas.user import UserRead
from services import auth_service
from services.security_log_service import log_event

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, payload.email, payload.password, payload.full_name)
    log_event(db, "register", user_id=user.id)
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    tokens = auth_service.create_session_tokens(user, db)
    log_event(db, "login", user_id=user.id, ip=request.client.host if request.client else None)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_tokens(db, payload.refresh_token)


@router.post("/logout")
def logout(payload: LogoutRequest, request: Request, db: Session = Depends(get_db)):
    auth_service.logout_user(db, payload.refresh_token)
    log_event(db, "logout", user_id=None, ip=request.client.host if request.client else None)
    return {"status": "ok"}


@router.get("/me", response_model=UserRead)
def me(user=Depends(get_current_user)):
    return user


@router.post("/master/verify")
def verify_master(payload: MasterVerifyRequest, user=Depends(get_current_user)):
    auth_service.verify_master_password(user, payload.password)
    return {"status": "verified"}
