from datetime import datetime, timedelta
from models.user import User
from utils.settings import get_settings

settings = get_settings()


def touch_user_activity(user: User):
    user.last_active_at = datetime.utcnow()


def ensure_user_active(user: User):
    if not user.last_active_at:
        return
    delta = datetime.utcnow() - user.last_active_at
    if delta > timedelta(minutes=settings.inactivity_lock_minutes):
        raise PermissionError("Session expired due to inactivity")
