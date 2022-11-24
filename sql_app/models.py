from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'potato_user'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    deleted_at = Column(TIMESTAMP)
    posts = relationship('Post', back_populates = 'user')


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key = True, index = True)
    content = Column(Text)
    title = Column(Text)
    user_id = Column(Integer, ForeignKey('potato_user.id'))
    user = relationship("User", back_populates="posts")