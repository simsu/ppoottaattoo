from sqlalchemy.orm import Session

from ..models.post import Post


def get_post(db: Session):
    return db.query(Post).order_by(Post.created.desc()).limit(5)


def create_post(db: Session, title: str, content: str):
    db_item = Post(title=title, content=content, user_id=3, post_type='eat')
    add = db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
