import os
import uuid
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from models.attachment import Attachment
from models.account import Account
from utils.file_crypto import encrypt_file, decrypt_file
from utils.settings import get_settings

settings = get_settings()


def save_attachment(db: Session, account: Account, file: UploadFile) -> Attachment:
    ext = os.path.splitext(file.filename or "upload.bin")[1]
    storage_name = f"{uuid.uuid4().hex}{ext}"
    os.makedirs(settings.attachments_dir, exist_ok=True)
    stored_path = os.path.join(settings.attachments_dir, storage_name)
    contents = file.file.read()
    encrypt_file(contents, stored_path)
    attachment = Attachment(
        account_id=account.id,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        stored_path=stored_path,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment


def get_attachment(db: Session, attachment_id: int, owner_id: int) -> Attachment:
    attachment = db.query(Attachment).join(Account).filter(
        Attachment.id == attachment_id,
        Account.owner_id == owner_id,
    ).first()
    if not attachment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    return attachment


def delete_attachment(db: Session, attachment_id: int, owner_id: int):
    attachment = get_attachment(db, attachment_id, owner_id)
    if os.path.exists(attachment.stored_path):
        os.remove(attachment.stored_path)
    db.delete(attachment)
    db.commit()


def read_attachment_data(attachment: Attachment) -> bytes:
    return decrypt_file(attachment.stored_path)


def list_attachments(db: Session, account_id: int, owner_id: int) -> list[Attachment]:
    return (
        db.query(Attachment)
        .join(Account)
        .filter(Attachment.account_id == account_id, Account.owner_id == owner_id)
        .all()
    )
