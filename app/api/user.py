from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import schemas, crud, services
from app.dependencies import get_db, get_session_user, cross_validate_user

user_router = APIRouter(
    prefix="/User"
)

@user_router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    :param user:    The user to create
    :param db:      The database session
    :return:
    """
    return services.user.create_user(user, db)


@user_router.get("/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_session_user)):
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
    return services.user.get_user_by_id(user_id, db)


# TODO: make this possibly use auth or user session once permissions are somehow added
#       to the system so that the amount of users returned can be limited, handle this in services
@user_router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of users
    :param skip:    The number of users to skip
    :param limit:   The maximum number of users to return
    :param db:      The database session
    :return:        A list of users
    """
    return services.user.get_users(skip=skip, limit=limit, db=db)


@user_router.put("/me", response_model=schemas.User)
def update_user_me(updates: schemas.UserUpdate,
                   current_user: schemas.User = Depends(cross_validate_user),
                   db: Session = Depends(get_db)):
    """
    Update any aspect of a user, including possibly password, username, or deactivating account.
    Requires authentication token.
    :param updates:
    :param current_user:
    :param db:
    :return:
    """

    return services.user.update_user(db, current_user.id, updates)


@user_router.delete("/me", response_model=schemas.User)
def delete_user_me(
                current_user: schemas.User = Depends(cross_validate_user),
                db: Session = Depends(get_db)):
    """
    Delete a user.
    Requires user to be logged in and provide username and password again for security reasons.
    :param current_user:
    :param db:
    :return:
    """

    return crud.user.delete(db, current_user.id)
