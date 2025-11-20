import secrets
import string


DEFAULT_CHARS = string.ascii_letters + string.digits + string.punctuation


def generate_password(length: int = 16, charset: str = DEFAULT_CHARS) -> str:
    if length < 8:
        raise ValueError("Password length must be >= 8")
    return "".join(secrets.choice(charset) for _ in range(length))
