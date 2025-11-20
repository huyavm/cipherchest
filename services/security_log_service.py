from sqlalchemy.orm import Session

from models.security_log import SecurityLog
from utils.settings import get_settings

settings = get_settings()


def log_event(db: Session, action: str, user_id: int | None = None, ip: str | None = None,
              user_agent: str | None = None, metadata: str | None = None):
    record = SecurityLog(
        user_id=user_id,
        action=action,
        ip_address=ip,
        user_agent=user_agent,
        metadata=metadata,
    )
    db.add(record)
    db.commit()

    if settings.telegram_bot_token and settings.telegram_chat_id:
        # placeholder for notification hook
        pass
