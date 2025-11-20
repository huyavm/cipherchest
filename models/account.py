from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship

from database.session import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_name = Column(String(255), index=True)
    provider = Column(String(255), index=True)
    account_type = Column(String(100), index=True)
    tags = Column(String(255), default="")
    status = Column(String(50), default="active")
    expires_at = Column(DateTime, nullable=True)
    category = Column(String(50), default="other")
    extra_metadata = Column(JSON, default=dict)
    encrypted_payload = Column(Text, nullable=False)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="accounts")
    attachments = relationship("Attachment", back_populates="account")
