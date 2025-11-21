from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, csrf_protect
from database.session import get_db
from schemas.account import AccountCreate, AccountRead, AccountUpdate
from services import account_service
from services.security_log_service import log_event

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountRead])
def list_accounts(
    search: str | None = None,
    tags: list[str] | None = Query(default=None),
    provider: str | None = None,
    account_type: str | None = None,
    expires_before: str | None = None,
    expires_after: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    accounts = account_service.list_accounts(
        db,
        owner_id=user.id,
        search=search,
        tags=tags,
        provider=provider,
        account_type=account_type,
        expires_before=expires_before,
        expires_after=expires_after,
    )
    return [account_service.to_schema(acc) for acc in accounts]


@router.post("", response_model=AccountRead, dependencies=[Depends(csrf_protect)])
def create_account(payload: AccountCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account = account_service.create_account(db, owner_id=user.id, payload=payload)
    log_event(db, "account_created", user_id=user.id, metadata=f"account:{account.id}")
    return account_service.to_schema(account)


@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account = account_service.get_account(db, user.id, account_id)
    return account_service.to_schema(account)


@router.put("/{account_id}", response_model=AccountRead, dependencies=[Depends(csrf_protect)])
def update_account(account_id: int, payload: AccountUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account = account_service.update_account(db, user.id, account_id, payload)
    log_event(db, "account_updated", user_id=user.id, metadata=f"account:{account.id}")
    return account_service.to_schema(account)


@router.delete("/{account_id}", dependencies=[Depends(csrf_protect)])
def delete_account(account_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account_service.delete_account(db, user.id, account_id)
    log_event(db, "account_deleted", user_id=user.id, metadata=f"account:{account_id}")
    return {"status": "deleted"}
