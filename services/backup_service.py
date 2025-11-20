import base64
import csv
import io
import json
import os
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.account import Account
from utils.file_crypto import encrypt_bytes, decrypt_bytes
from utils.settings import get_settings

settings = get_settings()


def export_backup(db: Session, owner_id: int, passphrase: str) -> str:
    accounts = db.query(Account).filter(Account.owner_id == owner_id).all()
    payload = []
    for acc in accounts:
        payload.append({
            "service_name": acc.service_name,
            "provider": acc.provider,
            "account_type": acc.account_type,
            "tags": acc.tags,
            "status": acc.status,
            "expires_at": acc.expires_at.isoformat() if acc.expires_at else None,
            "category": acc.category,
            "metadata": acc.extra_metadata,
            "notes": acc.notes,
            "encrypted_payload": acc.encrypted_payload,
        })
    serialized = json.dumps(payload).encode()
    blob = encrypt_bytes(serialized + passphrase.encode())
    os.makedirs(settings.backup_dir, exist_ok=True)
    filename = os.path.join(settings.backup_dir, f"backup-{datetime.utcnow().isoformat()}.bin")
    with open(filename, "wb") as f:
        f.write(blob)
    return base64.b64encode(blob).decode()


def import_backup(db: Session, owner_id: int, passphrase: str, payload: str):
    try:
        data = base64.b64decode(payload)
        decrypted = decrypt_bytes(data)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid archive") from exc
    if not decrypted.endswith(passphrase.encode()):
        raise HTTPException(status_code=400, detail="Passphrase mismatch")
    serialized = decrypted[: -len(passphrase)]
    items = json.loads(serialized.decode())
    for item in items:
        expires = item.get("expires_at")
        account = Account(
            owner_id=owner_id,
            service_name=item["service_name"],
            provider=item["provider"],
            account_type=item["account_type"],
            tags=item.get("tags", ""),
            status=item.get("status", "active"),
            category=item.get("category", "other"),
            expires_at=datetime.fromisoformat(expires) if expires else None,
            extra_metadata=item.get("metadata"),
            notes=item.get("notes"),
            encrypted_payload=item["encrypted_payload"],
        )
        db.add(account)
    db.commit()


def export_csv(db: Session, owner_id: int, account_type: str) -> str:
    accounts = (
        db.query(Account)
        .filter(Account.owner_id == owner_id, Account.account_type == account_type)
        .all()
    )
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "service_name", "provider", "status", "expires_at", "notes"])
    writer.writeheader()
    for item in accounts:
        writer.writerow({
            "id": item.id,
            "service_name": item.service_name,
            "provider": item.provider,
            "status": item.status,
            "expires_at": item.expires_at.isoformat() if item.expires_at else "",
            "notes": item.notes or "",
        })
    return output.getvalue()
