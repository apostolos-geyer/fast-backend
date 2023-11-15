from datetime import timedelta, datetime

from sqlalchemy.orm import Session

from app import models


def create(db: Session, user_id: int) -> models.UserSession:
    """
    Create a new session
    :param db:          The database session
    :param session:     The session to create
    :return:            The created session
    """

    db_session = models.UserSession(user_id=user_id, )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def read_by_id(db: Session, session_id: int) -> models.UserSession | None:
    """
    Get a session by its ID
    :param db:          The database session
    :param session_id:  The ID of the session to get
    :return:            The session with the given ID
    """
    return db.query(models.UserSession).filter(models.UserSession.session_id == session_id).first()


def read_by_user(db: Session, user_id: int) -> list[models.UserSession] | None:
    """
    Get all sessions for a user
    :param db:          The database session
    :param user_id:     The ID of the user
    :return:            A list of sessions for the user
    """
    return (db.query(models.UserSession).filter(models.UserSession.user_id == user_id).order_by(
        models.UserSession.created_at).all())


def read(db: Session, skip: int = 0, limit: int = 100) -> list[models.UserSession] | None:
    """
    Get all sessions
    :param db:          The database session
    :param skip:        The number of sessions to skip
    :param limit:       The maximum number of sessions to return
    :return:            A list of sessions
    """
    return db.query(models.UserSession).offset(skip).limit(limit).all()


def read_by_age(db: Session, age: timedelta) -> list[models.UserSession]:
    """
    Get all sessions older than a given timedelta
    :param db:          The database session
    :param age:         The age as a timedelta
    :return:            A list of sessions older than 'age'
    """
    cutoff_time = datetime.utcnow() - age
    return db.query(models.UserSession).filter(models.UserSession.created_at < cutoff_time).all()


def delete(db: Session, session_id: int) -> models.UserSession | None:
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


def delete_by_user(db: Session, user_id: int) -> int:
    """
    Delete all sessions for a user
    :param db:          The database session
    :param user_id:     The ID of the user
    :return:            A list of deleted sessions
    """
    result = db.query(models.UserSession).filter(models.UserSession.user_id == user_id).delete()

    db.commit()
    return result
