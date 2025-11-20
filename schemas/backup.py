from pydantic import BaseModel


class BackupRequest(BaseModel):
    passphrase: str


class RestoreRequest(BaseModel):
    passphrase: str
    payload: str
