from sqlalchemy.orm import Session

from ..models.post import SNS


def create_sns(db:Session, data: str):
    db_item = SNS(data=data, user_id=3)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
