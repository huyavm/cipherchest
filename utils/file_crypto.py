import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from hashlib import sha256

from utils.settings import get_settings

settings = get_settings()


def _key() -> bytes:
    return sha256(settings.encryption_master_key.encode()).digest()


def encrypt_bytes(data: bytes) -> bytes:
    aes = AESGCM(_key())
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, data, None)
    return nonce + ciphertext


def decrypt_bytes(data: bytes) -> bytes:
    aes = AESGCM(_key())
    nonce, ciphertext = data[:12], data[12:]
    return aes.decrypt(nonce, ciphertext, None)


def encrypt_file(source: bytes, destination: str):
    encrypted = encrypt_bytes(source)
    with open(destination, "wb") as f:
        f.write(encrypted)


def decrypt_file(path: str) -> bytes:
    with open(path, "rb") as f:
        data = f.read()
    return decrypt_bytes(data)


def encode_for_download(data: bytes) -> str:
    return base64.b64encode(data).decode()
