from fastapi import APIRouter, Depends

from api.dependencies import get_current_user, csrf_protect
from utils.password_generator import generate_password
from utils.totp import generate_totp_secret
from utils.hibp import is_password_pwned

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/password")
def password_generator(length: int = 16, user=Depends(get_current_user)):
    return {"password": generate_password(length=length)}


@router.post("/totp")
def totp_generator(account_name: str, issuer: str, user=Depends(get_current_user)):
    return generate_totp_secret(account_name, issuer)


@router.post("/hibp", dependencies=[Depends(csrf_protect)])
async def hibp(password: str, user=Depends(get_current_user)):
    pwned = await is_password_pwned(password)
    return {"pwned": pwned}
