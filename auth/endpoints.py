
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import security, schemas
from database import get_db


router = APIRouter(
    prefix="/token"
)

@router.post("/auth", response_model=schemas.Token)
def generate_auth_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login a user to get an authentication token
    :param form_data:   The form data containing the username and password
    :param db:          The database session
    :return:
    """
    user = security.verify_credentials(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    if not user.is_active:
        # update user status to active again
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token = security.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}