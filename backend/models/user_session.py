from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    # primary key for session is a uuid
    session_id = Column(Integer, unique=True, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=1), nullable=False)

    # foreign key for user
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_sessions")
