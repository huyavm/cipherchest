from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from models.token_session import TokenSession
from security.hashing import get_password_hash, verify_password
from security.jwt import create_token, decode_token, TokenError
from security.csrf import generate_csrf_token
from security.activity import touch_user_activity
from utils.settings import get_settings

settings = get_settings()


def register_user(db: Session, email: str, password: str, full_name: str) -> User:
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        email=email,
        full_name=full_name,
        role="user",
        hashed_password=get_password_hash(password),
        master_password_hash=get_password_hash(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User disabled")
    touch_user_activity(user)
    db.commit()
    return user


def create_session_tokens(user: User, db: Session) -> dict:
    access = create_token(str(user.id), settings.access_token_expire_minutes, "access", {"role": user.role})
    refresh = create_token(str(user.id), settings.refresh_token_expire_minutes, "refresh", {"role": user.role})
    session = TokenSession(
        user_id=user.id,
        refresh_jti=refresh["jti"],
        expires_at=datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes),
    )
    db.add(session)
    db.commit()
    csrf = generate_csrf_token(str(user.id))
    return {
        "access_token": access["token"],
        "refresh_token": refresh["token"],
        "csrf_token": csrf,
        "expires_in": settings.access_token_expire_minutes * 60,
        "role": user.role,
        "user": {"id": user.id, "email": user.email, "full_name": user.full_name},
    }


def refresh_tokens(db: Session, refresh_token: str) -> dict:
    try:
        payload = decode_token(refresh_token)
    except TokenError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    jti = payload.get("jti")
    session = db.query(TokenSession).filter(TokenSession.refresh_jti == jti).first()
    if not session or session.is_revoked or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_session_tokens(user, db)


def logout_user(db: Session, refresh_token: str):
    try:
        payload = decode_token(refresh_token)
    except TokenError:
        return
    jti = payload.get("jti")
    session = db.query(TokenSession).filter(TokenSession.refresh_jti == jti).first()
    if session:
        session.is_revoked = True
        db.commit()


def verify_master_password(user: User, password: str):
    if not verify_password(password, user.master_password_hash):
        raise HTTPException(status_code=403, detail="Invalid master password")
