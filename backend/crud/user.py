from sqlalchemy.orm import Session

from backend import models


def create(db: Session, user: dict) -> models.User | None:
    """
    Create a new user
    :param db:      The database session
    :param user:    The user to create
    :return:        The created user
    """
    # TODO handle errors adding to db

    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_by_id(db: Session, user_id: int) -> models.User | None:
    """
    Get a user by their ID
    :param db:          The database session
    :param user_id:     The ID of the user to get
    :return:            The user with the given ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def read_by_session_id(db: Session, session_id: int) -> models.User | None:
    """
    Get a user by their session ID
    :param db:          The database session
    :param session_id:  The ID of the session to get the user for
    :return:            The user with the given session ID
    """
    db_session = db.query(models.UserSession).filter(
        models.UserSession.session_id == session_id).first()
    if db_session:
        return db_session.user
    else:
        return None


def read_by_username(db: Session, username: str) -> models.User | None:
    """
    Get a user by their username
    :param db:          The database session
    :param username:    The username of the user to get
    :return:            The user with the given username
    """
    if username is None: return None
    return db.query(models.User).filter(models.User.username == username).first()


def read_by_email(db: Session, email: str) -> models.User | None:
    """
    Get a user by their email address
    :param db:          The database session
    :param email:       The email address of the user to get
    :return:            The user with the given email address
    """
    if email is None: return None
    return db.query(models.User).filter(models.User.email == email).first()


def read(db: Session, skip: int = 0, limit: int = 100) -> list[models.User] | None:
    """
    Get all users
    :param db:          The database session
    :param skip:        The number of users to skip
    :param limit:       The maximum number of users to return
    :return:            A list of users
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def update(db: Session, db_user: models.User, update_data: dict) -> models.User | None:
    # if new password is set it will be in hashed_password already set from the service layer
    # all other dict keys will be same name as column in db
    # so we can just set them all at once
    for key, value in update_data.items():
        setattr(db_user, key, value)


    db.commit()
    db.refresh(db_user)
    return db_user


def delete(db: Session, user_id: int) -> models.User:
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


