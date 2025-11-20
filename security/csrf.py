from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from utils.settings import get_settings

settings = get_settings()
serializer = URLSafeTimedSerializer(secret_key=settings.csrf_secret)


def generate_csrf_token(identity: str) -> str:
    return serializer.dumps(identity)


def validate_csrf(token: str, max_age: int = 3600) -> str:
    try:
        return serializer.loads(token, max_age=max_age)
    except SignatureExpired as exc:
        raise ValueError("CSRF token expired") from exc
    except BadSignature as exc:
        raise ValueError("Invalid CSRF token") from exc
