from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class SensitiveData(BaseModel):
    login_email: str | None = None
    login_username: str | None = None
    password: str | None = None
    recovery_email: str | None = None
    recovery_phone: str | None = None
    two_fa_secret: str | None = None
    two_fa_type: str | None = None
    backup_codes: list[str] = Field(default_factory=list)
    totp_devices: list[str] = Field(default_factory=list)
    app_passwords: list[str] = Field(default_factory=list)
    security_questions: list[dict[str, str]] = Field(default_factory=list)
    api_key: str | None = None
    token: str | None = None
    ssh_user: str | None = None
    ssh_password: str | None = None
    ssh_private_key: str | None = None
    ssh_public_key: str | None = None
    ip_address: str | None = None
    port: str | None = None
    card_holder: str | None = None
    card_type: str | None = None
    card_last4: str | None = None
    card_expiry: str | None = None
    card_cvv: str | None = None
    billing_address: str | None = None
    linked_accounts: list[str] = Field(default_factory=list)
    payment_history: list[dict[str, Any]] = Field(default_factory=list)
    bypass_codes: list[str] = Field(default_factory=list)


class AccountBase(BaseModel):
    service_name: str
    provider: str
    account_type: str
    tags: list[str] = Field(default_factory=list)
    status: str = "active"
    expires_at: datetime | None = None
    category: str = "other"
    metadata: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class AccountCreate(AccountBase):
    sensitive: SensitiveData


class AccountUpdate(BaseModel):
    service_name: str | None = None
    provider: str | None = None
    account_type: str | None = None
    tags: list[str] | None = None
    status: str | None = None
    expires_at: datetime | None = None
    category: str | None = None
    metadata: dict[str, Any] | None = None
    notes: str | None = None
    sensitive: SensitiveData | None = None


class AccountRead(AccountBase):
    id: int
    owner_id: int
    sensitive: SensitiveData
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
