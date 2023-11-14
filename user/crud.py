# USER CRUD OPERATIONS
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

import auth.security
from . import schemas, models



#
# CRUD operations for the User model
#

# CREATE method

def create_user(db: Session, user: schemas.UserCreate) -> models.User | None:
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
        hashed_password=auth.security.get_password_hash(user.password),
        is_active=True  # Assuming you want new users to be active by default
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# READ methods

def get_user(db: Session, user_id: int) -> models.User | None:
    """
    Get a user by their ID
    :param db:          The database session
    :param user_id:     The ID of the user to get
    :return:            The user with the given ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_session(db: Session, session_id: int) -> models.User | None:
    """
    Get a user by their session ID
    :param db:          The database session
    :param session_id:  The ID of the session to get the user for
    :return:            The user with the given session ID
    """
    db_session = db.query(models.UserSession).filter(models.UserSession.session_id == session_id).first()
    if db_session:
        return db_session.user
    else:
        return None


def get_user_by_username(db: Session, username: str) -> models.User | None:
    """
    Get a user by their username
    :param db:          The database session
    :param username:    The username of the user to get
    :return:            The user with the given username
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """
    Get a user by their email address
    :param db:          The database session
    :param email:       The email address of the user to get
    :return:            The user with the given email address
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User] | None:
    """
    Get all users
    :param db:          The database session
    :param skip:        The number of users to skip
    :param limit:       The maximum number of users to return
    :return:            A list of users
    """
    return db.query(models.User).offset(skip).limit(limit).all()


# UPDATE methods
# TODO: add a UserUpdate schema and update_user method, as well as necessary endpoints, auth methods, schemas, etc.
def update_user(db: Session, user_id: int, update: schemas.UserUpdate) -> models.User | None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = update.model_dump(exclude_unset=True)

        if 'new_username' in update_data and update_data['new_username']:
            # verify username is unique
            other_user = db.query(models.User).filter(models.User.username == update_data['new_username']).first()
            if other_user:
                raise ValueError("Username is already taken")

        if 'new_password' in update_data and update_data['new_password']:
            hashed_password = auth.security.get_password_hash(update_data['new_password'])
            db_user.hashed_password = hashed_password

        for key, value in update_data.items():

            if key not in ['new_password', 'new_password2']:  # Exclude password fields
                key = key.replace('new_', '')  # Remove 'new_' prefix from keys
                setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
    return db_user


# DELETE methods
def delete_user(db: Session, user_id: int) -> models.User:
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


#
# CRUD operations for the Session model
#

# create
def create_session(db: Session, user_id: int) -> models.UserSession:
    """
    Create a new session
    :param db:          The database session
    :param session:     The session to create
    :return:            The created session
    """
    # check how many sessions user currently has
    # if more than 5, delete oldest session

    users_current_sessions = get_sessions_by_user(db, user_id)
    if users_current_sessions is not None and len(users_current_sessions) >= 5:
        oldest_session = users_current_sessions[0]
        delete_session(db, oldest_session.session_id)

    db_session = models.UserSession(
        user_id=user_id,
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

# read functions
def get_session(db: Session, session_id: int) -> models.UserSession | None:
    """
    Get a session by its ID
    :param db:          The database session
    :param session_id:  The ID of the session to get
    :return:            The session with the given ID
    """
    return db.query(models.UserSession).filter(models.UserSession.session_id == session_id).first()

def get_sessions_by_user(db: Session, user_id: int) -> list[models.UserSession] | None:
    """
    Get all sessions for a user
    :param db:          The database session
    :param user_id:     The ID of the user
    :return:            A list of sessions for the user
    """
    return (db.query(models.UserSession).filter(models.UserSession.user_id == user_id)
            .order_by(models.UserSession.created_at).all())

def get_sessions(db: Session, skip: int = 0, limit: int = 100) -> list[models.UserSession] | None:
    """
    Get all sessions
    :param db:          The database session
    :param skip:        The number of sessions to skip
    :param limit:       The maximum number of sessions to return
    :return:            A list of sessions
    """
    return db.query(models.UserSession).offset(skip).limit(limit).all()

def get_sessions_older_than(db: Session, age: timedelta) -> list[models.UserSession]:
    """
    Get all sessions older than a given timedelta
    :param db:          The database session
    :param age:         The age as a timedelta
    :return:            A list of sessions older than 'age'
    """
    cutoff_time = datetime.utcnow() - age
    return db.query(models.UserSession).filter(models.UserSession.created_at < cutoff_time).all()

# delete session
def delete_session(db: Session, session_id: int) -> models.UserSession | None:
    """
    Delete a session by its ID
    :param db:          The database session
    :param session_id:  The ID of the session to delete
    :return:            The deleted session
    """
    db_session = db.query(models.UserSession).filter(models.UserSession.session_id == session_id).first()
    if db_session:
        db.delete(db_session)
        db.commit()
    return db_session

# delete sessions for user
def delete_sessions_by_user(db: Session, user_id: int) -> list[models.UserSession] | None:
    """
    Delete all sessions for a user
    :param db:          The database session
    :param user_id:     The ID of the user
    :return:            A list of deleted sessions
    """
    db_sessions = db.query(models.UserSession).filter(models.UserSession.user_id == user_id).all()
    for db_session in db_sessions:
        db.delete(db_session)
    db.commit()
    return db_sessions


