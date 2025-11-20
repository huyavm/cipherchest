from fastapi import Depends, Header, HTTPException, status, Request
from sqlalchemy.orm import Session

from database.session import get_db
from models.user import User
from security.jwt import decode_token, TokenError
from security.activity import ensure_user_active, touch_user_activity
from security.csrf import validate_csrf
from utils.settings import get_settings

settings = get_settings()


def get_current_user(db: Session = Depends(get_db), authorization: str | None = Header(default=None)) -> User:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = authorization.replace("Bearer ", "")
    try:
        payload = decode_token(token)
    except TokenError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        ensure_user_active(user)
    except PermissionError as exc:
        raise HTTPException(status_code=440, detail=str(exc)) from exc
    touch_user_activity(user)
    db.commit()
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return user


def csrf_protect(request: Request, csrf_token: str | None = Header(default=None, alias="csrf-token")):
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        if not csrf_token:
            raise HTTPException(status_code=403, detail="Missing CSRF token")
        try:
            validate_csrf(csrf_token)
        except ValueError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
