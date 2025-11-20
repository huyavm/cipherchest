from datetime import datetime
from sqlalchemy.orm import Query
from sqlalchemy import or_, func

from models.account import Account


def apply_account_filters(query: Query, search: str | None = None, tags: list[str] | None = None,
                          provider: str | None = None, account_type: str | None = None,
                          expires_before: str | None = None, expires_after: str | None = None):
    if search:
        like = f"%{search.lower()}%"
        query = query.filter(
            or_(func.lower(Account.service_name).like(like), func.lower(Account.provider).like(like))
        )
    if tags:
        for tag in tags:
            query = query.filter(Account.tags.like(f"%{tag}%"))
    if provider:
        query = query.filter(Account.provider == provider)
    if account_type:
        query = query.filter(Account.account_type == account_type)
    if expires_before:
        try:
            before = datetime.fromisoformat(expires_before)
            query = query.filter(Account.expires_at <= before)
        except ValueError:
            pass
    if expires_after:
        try:
            after = datetime.fromisoformat(expires_after)
            query = query.filter(Account.expires_at >= after)
        except ValueError:
            pass
    return query
