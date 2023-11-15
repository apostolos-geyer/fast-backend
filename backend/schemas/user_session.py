from datetime import datetime
from pydantic import BaseModel


class SessionBase(BaseModel):
    session_id: str
    created_at: datetime
    expires_at: datetime


class SessionCreate(SessionBase):
    user_id: int


class SessionInDB(SessionCreate):
    class Config:
        from_attributes = True