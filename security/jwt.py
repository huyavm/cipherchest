from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from jose import jwt, JWTError
import uuid

from utils.settings import get_settings

settings = get_settings()


class TokenError(Exception):
    pass


def create_token(subject: str, expires_minutes: int, token_type: str, extra: Dict[str, Any] | None = None) -> dict:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    payload = {
        "sub": subject,
        "exp": expire,
        "iat": now,
        "type": token_type,
        "jti": str(uuid.uuid4()),
    }
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return {"token": token, "expires_at": expire, "jti": payload["jti"]}


def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as exc:
        raise TokenError("Invalid token") from exc
