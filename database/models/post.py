from sqlalchemy import Column, Text, TIMESTAMP, Integer, ForeignKey, JSON
import datetime
from sqlalchemy.orm import relationship

from .. import Base


class Post(Base):
    __tablename__ = 'post'

    def __repr__(self):
        return f'{{id: {self.id}, title: {self.title}}}'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created = Column('created_at', TIMESTAMP, nullable=False, default=datetime.datetime.now)
    updated = Column('updated_at', TIMESTAMP, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    post_type = Column('post_type', nullable=False)
    view_count = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, ForeignKey('potato_user.id'))
    user = relationship('User', back_populates='posts')


class User(Base):
    __tablename__ = 'potato_user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, nullable=False)
    posts = relationship('Post', back_populates='user')


class SNS(Base):
    __tablename__ = 'sns'

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, nullable=False)
    user_id = Column(Integer, ForeignKey('potato_user.id'))
