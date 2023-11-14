from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from database import get_db
from . import schemas, crud, models, dependencies as dep
from auth import dependencies as auth_dep

user_router = APIRouter(prefix="/user")


@user_router.post("/login")
def login(
        response: Response,
        user: models.User = Depends(dep.authenticate_user),
        db: Session = Depends(get_db),
):
    """
    Login a user to get an authentication token
    :param response:
    :param user:
    :param db:
    :return:
    """
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    user_session = crud.create_session(db, user.id)

    # Set a cookie with the session ID, that the client's browser will store.
    response.set_cookie(key="session_id", value=str(user_session.session_id), httponly=True)  # httponly helps with security
    return {"message": "Logged in successfully"}


@user_router.post("/logout")
def logout(
        response: Response,  # Inject the Response object to delete the cookie
        current_user: models.User = Depends(dep.get_session_user),
        db: Session = Depends(get_db),
):

    user_sessions = crud.get_sessions_by_user(db, current_user.id)
    if user_sessions is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No sessions to delete")

    else:
        # deletes all user sessions upon logout for increased security
        crud.delete_sessions_by_user(db, current_user.id)

    # Delete the cookie by setting its value to None
    response.delete_cookie(key="session_id")
    return {"message": "Logged out successfully"}


@user_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    :param user:    The user to create
    :param db:      The database session
    :return:
    """
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    elif crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        return crud.create_user(db, user)

@user_router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(dep.get_session_user)):
    """
    Get the current user using the access token
    :param current_user:
    :return:
    """
    return current_user

@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID
    :param user_id:     The ID of the user to get
    :param db:          The database session
    :return:            The user with the given ID
    """
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@user_router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of users
    :param skip:    The number of users to skip
    :param limit:   The maximum number of users to return
    :param db:      The database session
    :return:        A list of users
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# TODO: implement update and delete endpoints.
@user_router.put("/me", response_model=schemas.User)
def update_user_me(updates: schemas.UserUpdate,
                   current_user_token: models.User = Depends(auth_dep.get_token_user),
                   current_user_session: models.User = Depends(dep.get_session_user),
                   db: Session = Depends(get_db)):
    """
    Update any aspect of a user, including possibly password, username, or deactivating account.
    Requires authentication token.
    :param updates:
    :param current_user_token: the current user, as determined by the authentication token
    :param db:
    :return:
    """
    if current_user_token.id != current_user_session.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Error")

    return crud.update_user(db, current_user_token.id, updates)

@user_router.delete("/me", response_model=schemas.User)
def delete_user_me(
                current_user: schemas.User = Depends(auth_dep.get_token_user),
                db: Session = Depends(get_db)):
    """
    Delete a user.
    Requires user to be logged in and provide username and password again for security reasons.
    :param form_data:
    :param db:
    :return:
    """

    return crud.delete_user(db, current_user.id)

