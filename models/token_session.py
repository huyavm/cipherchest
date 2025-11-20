from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

from database.session import Base


class TokenSession(Base):
    __tablename__ = "token_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    refresh_jti = Column(String(64), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def is_valid(self) -> bool:
        return not self.is_revoked and self.expires_at > datetime.utcnow()
