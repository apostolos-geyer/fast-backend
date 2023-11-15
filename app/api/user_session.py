from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, services
from app.dependencies import get_db, authenticate_user, get_session_user

session_router = APIRouter(
    prefix="/session"
)


@session_router.post("/auth", response_model=schemas.Token)
def generate_auth_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login a user to get an authentication token
    :param form_data:   The form data containing the username and password
    :param db:          The database session
    :return:
    """
    user = services.user.verify_credentials(form_data, db)
    access_token = services.user_session.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@session_router.post("/login")
def login(
        response: Response,
        user: schemas.User = Depends(authenticate_user),
        db: Session = Depends(get_db),
):
    """
    Login a user to get an authentication token
    :param response:
    :param user:
    :param db:
    :return:
    """
    user_session = services.user_session.session_login(user, db)
    response.set_cookie(key="session_id", value=str(user_session.session_id),
                        httponly=True)  # http only helps with security
    return {"message": "Logged in successfully"}


@session_router.post("/logout")
def logout(
        response: Response,  # Inject the Response object to delete the cookie
        current_user: schemas.User = Depends(get_session_user),
        db: Session = Depends(get_db),
):

    services.user_session.session_logout(current_user, db)
    response.delete_cookie(key="session_id")
    return {"message": "Logged out successfully"}
