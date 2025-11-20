import base64
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from hashlib import sha256

from utils.settings import get_settings

settings = get_settings()


def _derive_key() -> bytes:
    raw_key = settings.encryption_master_key.encode()
    return sha256(raw_key).digest()


def encrypt_payload(data: dict) -> str:
    key = _derive_key()
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    serialized = json.dumps(data).encode()
    ciphertext = aesgcm.encrypt(nonce, serialized, None)
    payload = base64.b64encode(nonce + ciphertext).decode()
    return payload


def decrypt_payload(payload: str) -> dict:
    if not payload:
        return {}
    key = _derive_key()
    decoded = base64.b64decode(payload)
    nonce, ciphertext = decoded[:12], decoded[12:]
    aesgcm = AESGCM(key)
    data = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(data.decode())
