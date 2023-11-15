from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from backend.database import Base


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
