from datetime import datetime
from pydantic import BaseModel


class AttachmentRead(BaseModel):
    id: int
    filename: str
    content_type: str
    created_at: datetime

    class Config:
        from_attributes = True
