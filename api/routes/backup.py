from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, csrf_protect
from database.session import get_db
from schemas.backup import BackupRequest, RestoreRequest
from services.backup_service import export_backup, import_backup, export_csv

router = APIRouter(prefix="/backup", tags=["backup"], dependencies=[Depends(csrf_protect)])


@router.post("/export")
def export_data(payload: BackupRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    blob = export_backup(db, user.id, payload.passphrase)
    return {"payload": blob}


@router.post("/import")
def import_data(payload: RestoreRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    import_backup(db, user.id, payload.passphrase, payload.payload)
    return {"status": "restored"}


@router.get("/csv/{account_type}")
def export_accounts_csv(account_type: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    content = export_csv(db, user.id, account_type)
    return Response(content=content, media_type="text/csv")
