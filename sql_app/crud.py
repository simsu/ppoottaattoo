from sqlalchemy.orm import Session
import datetime

from . import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    now = datetime.datetime.now()
    db_user = models.User(
        username = user.username,
        created_at = now,
        updated_at = now,
        deleted_at= None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()
