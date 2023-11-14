from datetime import datetime, timedelta
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class User(Base):
    __tablename__ = "users"

    # primary key for user, sequential unique integers
    id = Column(Integer, primary_key=True, index=True)

    # identifiers for user
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    display_name = Column(String(255), unique=False, index=False)

    # user status
    is_active = Column(Boolean, default=True)

    # hashed password
    hashed_password = Column(String(255))

    # users have sessions, 1, or more
    user_sessions = relationship("UserSession", back_populates="user")


class UserSession(Base):
    __tablename__ = "user_sessions"

    # primary key for session is a uuid
    session_id = Column(Integer, unique=True, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=1), nullable=False)

    # foreign key for user
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_sessions")





