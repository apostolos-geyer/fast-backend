from datetime import timedelta, datetime
from typing import Optional
from fastapi import Response

import jwt
from sqlalchemy.orm import Session

from app import schemas, crud
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.errors import UserAuthorizationError


def cross_validate_user(session_user: schemas.User,
                        token_user: schemas.User):
    if session_user.id != token_user.id:
        raise UserAuthorizationError("User associated with session does not match user associated with token\n"
                                     "Something is very wrong.")
    return session_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def session_login(user: schemas.User, db: Session):
    user_session = crud.user_session.create(db, user.id)

    users_current_sessions = crud.user_session.read_by_user(db, user.id)
    if users_current_sessions is not None and len(users_current_sessions) >= 5:
        oldest_session = users_current_sessions[0]
        crud.user_session.delete(db, oldest_session.session_id)
    # Set a cookie with the session ID, that the client's browser will store.
    return user_session


def session_logout(user: schemas.User, db: Session):
    user_sessions = crud.user_session.read_by_user(db, user.id)
    if user_sessions is None:
        raise UserAuthorizationError("No sessions to delete")
    else:
        crud.user_session.delete_by_user(db, user.id)
    return True


