from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.session import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    stored_path = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="attachments")
