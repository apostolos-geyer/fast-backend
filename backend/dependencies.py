from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import schemas, services
from backend.config import oauth2_scheme
from backend.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> schemas.User:
    return services.user.verify_credentials(form_data, db)

def get_token_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> schemas.User:
    return services.user.get_user_by_token(token, db)


def get_session_user(request: Request, db: Session = Depends(get_db)) -> schemas.User:
    return services.user.get_user_by_session(request, db)


def cross_validate_user(session_user: schemas.User = Depends(get_session_user),
                        token_user: schemas.User = Depends(get_token_user)) -> schemas.User:
    return services.user_session.cross_validate_user(session_user, token_user)
