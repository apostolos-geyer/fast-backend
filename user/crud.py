# USER CRUD OPERATIONS
from sqlalchemy.orm import Session
from . import models, schemas, auth

# CREATE method

def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    """
    Create a new user
    :param db:      The database session
    :param user:    The user to create
    :return:        The created user
    """
    # If display_name is not provided, default it to the username
    display_name = user.display_name if user.display_name else user.username
    db_user = models.User(
        username=user.username,
        email=user.email,
        display_name=display_name,
        hashed_password=auth.get_password_hash(user.password),
        is_active=True  # Assuming you want new users to be active by default
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# READ methods

def get_user(db: Session, user_id: int) -> schemas.User:
    """
    Get a user by their ID
    :param db:          The database session
    :param user_id:     The ID of the user to get
    :return:            The user with the given ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> schemas.User:
    """
    Get a user by their username
    :param db:          The database session
    :param username:    The username of the user to get
    :return:            The user with the given username
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> schemas.User:
    """
    Get a user by their email address
    :param db:          The database session
    :param email:       The email address of the user to get
    :return:            The user with the given email address
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[schemas.User]:
    """
    Get all users
    :param db:          The database session
    :param skip:        The number of users to skip
    :param limit:       The maximum number of users to return
    :return:            A list of users
    """
    return db.query(models.User).offset(skip).limit(limit).all()


# UPDATE methods
def update_user(db: Session, user_id: int, update: schemas.UserUpdate) -> models.User:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = update.dict(exclude_unset=True)
        if 'password' in update_data and update_data['password']:
            hashed_password = auth.get_password_hash(update_data['password'])
            db_user.hashed_password = hashed_password

        for key, value in update_data.items():
            if key not in ['password', 'password2']:  # Exclude password fields
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
    return db_user


# DELETE methods

def delete_user(db: Session, user_id: int) -> schemas.User:
    """
    Delete a user by their ID
    :param db:          The database session
    :param user_id:     The ID of the user to delete
    :return:            The deleted user
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

