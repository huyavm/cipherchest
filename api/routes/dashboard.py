from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user
from database.session import get_db
from schemas.dashboard import DashboardStats
from services.dashboard_service import dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return dashboard_stats(db, user.id)
