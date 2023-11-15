import jwt
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.config import SECRET_KEY, ALGORITHM, pwd_context
from backend.errors import UserCreationError, UserNotFoundError, UserAuthorizationError, UserUpdateError


def create_user(user: schemas.UserCreate, db: Session) -> schemas.User:
    """
    Create a new user
    :param user:    The user to create
    :param db:      The database session
    :return:
    """
    if error := next((msg for msg, check in [
        ("Email already registered", crud.user.read_by_email(db, user.email)),
        ("Username already registered", crud.user.read_by_username(db, user.username))
    ] if check), None):
        raise UserCreationError(error)

    user = {
        "username": user.username,
        "email": user.email,
        "display_name": user.display_name if user.display_name else user.username,
        "hashed_password": pwd_context.hash(user.password),
        "is_active": True,
    }

    return crud.user.create(db, user)


def get_user_by_id(user_id: int, db: Session) -> schemas.User:
    """
    Get a user by their ID
    :param user_id:     The ID of the user to get
    :param db:          The database session
    :return:            The user with the given ID
    """
    if db_user := crud.user.read_by_id(db, user_id):
        return db_user
    else:
        raise UserNotFoundError(f"Could not find user with ID {user_id}")


# TODO: make this possibly use auth or user session once permissions are somehow added
#       to the system so that the amount of users returned can be limited
def get_users(skip: int = 0, limit: int = 100, db: Session = None) -> list[schemas.User]:
    """
    Get a list of users
    :param skip:    The number of users to skip
    :param limit:   The maximum number of users to return
    :param db:      The database session
    :return:        A list of users
    """
    return crud.user.read(db, skip=skip, limit=limit)


def update_user(db: Session, user_id: int, update: schemas.UserUpdate) -> schemas.User:
    try:
        if not (db_user := crud.user.read_by_id(db, user_id)):
            raise UserNotFoundError(f"User not found for ID: {user_id}")
    except UserNotFoundError as user_error:
        raise UserUpdateError(f"Authorization error: {user_error}") from user_error

    update_data = update.model_dump(exclude_unset=True)

    if ('new_email' in update_data
            and update_data['new_email']
            and crud.user.read_by_email(db, update_data['new_email'])):
        raise UserUpdateError("Email is already taken")

    if ('new_username' in update_data
            and update_data['new_username']
            and crud.user.read_by_username(db, update_data['new_username'])):
        raise UserUpdateError("Username is already taken")

    if ('new_password' in update_data
            and update_data['new_password']):
        hashed_password = pwd_context.hash(update_data['new_password'])
        update_data['hashed_password'] = hashed_password

    # remove new_password and new_password2 from update_data, and drop new_ from the rest of the keys
    update_data = {key.replace('new_', ''): value for key, value in update_data.items()
                      if key != 'new_password'}

    return crud.user.update(db, db_user, update_data)


def get_user_by_session(request: Request, db: Session) -> schemas.User:
    """
    Get a user by their session ID
    :param request:    The request to get the session ID from
    :param db:          The database session
    :return:            The user with the given session ID
    """
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise UserAuthorizationError("User is not logged in.")
    elif not (session := crud.user_session.read_by_id(db, int(session_id))):
        raise UserAuthorizationError("Could not find session.")

    return session.user


def get_user_by_token(token: str, db: Session) -> schemas.User:
    """
    Get a user by their token
    :param token:   The token to get the user for
    :param db:      The database session
    :return:        The user with the given token
    """
    if token is None:
        raise UserAuthorizationError("Temporary authorization token not found.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        user = crud.user.read_by_username(db, username)
        if user is None:
            raise UserNotFoundError(f"User not found for username: {username} (Token: {token})")

    except UserNotFoundError as user_error:
        raise UserAuthorizationError(f"Authorization error: {user_error}") from user_error

    except jwt.PyJWTError as jwt_error:
        raise UserAuthorizationError(f"Token decoding error: {jwt_error}") from jwt_error

    except Exception as e:
        # Catch any other unexpected exceptions and re-raise as UserAuthorizationError
        raise UserAuthorizationError(f"Unexpected error: {e}") from e

    return user


def verify_credentials(form_data: OAuth2PasswordRequestForm, db: Session) -> schemas.User:
    """
    Verify the credentials of a user
    :param form_data:   The credentials to verify
    :param db:          The database session
    :return:            The user with the given credentials
    """
    try:
        if not (db_user := crud.user.read_by_username(db, form_data.username)):
            raise UserNotFoundError(f"User not found for username: {form_data.username}")
    except UserNotFoundError as user_error:
        raise UserAuthorizationError(f"Authorization error: {user_error}") from user_error

    hashed_password = db_user.hashed_password
    if not pwd_context.verify(form_data.password, hashed_password):
        raise UserAuthorizationError("Incorrect password")

    return db_user
