from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.account import Account
from schemas.account import AccountCreate, AccountUpdate, AccountRead
from security.encryption import encrypt_payload, decrypt_payload
from utils.filters import apply_account_filters


def _serialize_tags(tags: list[str]) -> str:
    return ",".join(sorted(set(tags)))


def _deserialize_tags(tag_string: str | None) -> list[str]:
    if not tag_string:
        return []
    return [t for t in tag_string.split(",") if t]


def create_account(db: Session, owner_id: int, payload: AccountCreate) -> Account:
    encrypted = encrypt_payload(payload.sensitive.model_dump())
    account = Account(
        owner_id=owner_id,
        service_name=payload.service_name,
        provider=payload.provider,
        account_type=payload.account_type,
        tags=_serialize_tags(payload.tags),
        status=payload.status,
        expires_at=payload.expires_at,
        category=payload.category,
        extra_metadata=payload.metadata,
        encrypted_payload=encrypted,
        notes=payload.notes,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def list_accounts(db: Session, owner_id: int, **filters) -> Sequence[Account]:
    query = db.query(Account).filter(Account.owner_id == owner_id)
    query = apply_account_filters(query, **filters)
    return query.order_by(Account.updated_at.desc()).all()


def get_account(db: Session, owner_id: int, account_id: int) -> Account:
    account = db.query(Account).filter(Account.owner_id == owner_id, Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


def update_account(db: Session, owner_id: int, account_id: int, payload: AccountUpdate) -> Account:
    account = get_account(db, owner_id, account_id)
    for field in ["service_name", "provider", "account_type", "status", "expires_at", "category", "notes"]:
        value = getattr(payload, field)
        if value is not None:
            setattr(account, field, value)
    if payload.metadata is not None:
        account.extra_metadata = payload.metadata
    if payload.tags is not None:
        account.tags = _serialize_tags(payload.tags)
    if payload.sensitive is not None:
        account.encrypted_payload = encrypt_payload(payload.sensitive.model_dump())
    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, owner_id: int, account_id: int):
    account = get_account(db, owner_id, account_id)
    db.delete(account)
    db.commit()


def to_schema(account: Account) -> AccountRead:
    sensitive = decrypt_payload(account.encrypted_payload)
    return AccountRead(
        id=account.id,
        owner_id=account.owner_id,
        service_name=account.service_name,
        provider=account.provider,
        account_type=account.account_type,
        tags=_deserialize_tags(account.tags),
        status=account.status,
        expires_at=account.expires_at,
        category=account.category,
        metadata=account.extra_metadata or {},
        notes=account.notes,
        sensitive=sensitive,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )
