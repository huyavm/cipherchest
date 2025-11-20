from fastapi import APIRouter, Depends, UploadFile, File, Response
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, csrf_protect
from database.session import get_db
from services import account_service
from services.attachment_service import save_attachment, get_attachment, read_attachment_data, delete_attachment, list_attachments
from schemas.attachment import AttachmentRead

router = APIRouter(prefix="/attachments", tags=["attachments"])


@router.post("/accounts/{account_id}", dependencies=[Depends(csrf_protect)])
def upload_attachment(account_id: int, upload: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    account = account_service.get_account(db, user.id, account_id)
    attachment = save_attachment(db, account, upload)
    return {"id": attachment.id, "filename": attachment.filename}


@router.get("/accounts/{account_id}", response_model=list[AttachmentRead])
def list_account_attachments(account_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account_service.get_account(db, user.id, account_id)
    return list_attachments(db, account_id, user.id)


@router.get("/{attachment_id}")
def download_attachment(attachment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    attachment = get_attachment(db, attachment_id, user.id)
    data = read_attachment_data(attachment)
    return Response(content=data, media_type=attachment.content_type, headers={
        "Content-Disposition": f"attachment; filename={attachment.filename}"
    })


@router.delete("/{attachment_id}", dependencies=[Depends(csrf_protect)])
def remove_attachment(attachment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    delete_attachment(db, attachment_id, user.id)
    return {"status": "deleted"}
