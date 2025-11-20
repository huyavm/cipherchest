from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.account import Account
from security.encryption import decrypt_payload


def dashboard_stats(db: Session, owner_id: int) -> dict:
    total = db.query(Account).filter(Account.owner_id == owner_id).count()
    upcoming = (
        db.query(Account)
        .filter(Account.owner_id == owner_id, Account.expires_at.isnot(None), Account.expires_at <= datetime.utcnow() + timedelta(days=14))
        .count()
    )
    accounts = db.query(Account).filter(Account.owner_id == owner_id).all()
    without_2fa = 0
    category_counts: dict[str, int] = {}
    for acc in accounts:
        sensitive = decrypt_payload(acc.encrypted_payload)
        if not sensitive.get("two_fa_secret"):
            without_2fa += 1
        category_counts[acc.category] = category_counts.get(acc.category, 0) + 1
    return {
        "total_accounts": total,
        "expiring_accounts": upcoming,
        "without_two_fa": without_2fa,
        "by_category": category_counts,
    }
