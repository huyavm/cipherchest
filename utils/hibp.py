import hashlib
import httpx

from utils.settings import get_settings

settings = get_settings()


async def is_password_pwned(password: str) -> bool:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    url = f"{settings.hibp_api_url}{prefix}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers={"Add-Padding": "true"})
        resp.raise_for_status()
        for line in resp.text.splitlines():
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                return True
    return False
