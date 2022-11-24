from pydantic import BaseModel


class PostBase(BaseModel):
    id: int
    content: str
    title: str
    post_type: str
    view_count: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    username: str


class User(UserBase):
    username: str
    posts: list[PostBase] | None = None

    class Config:
        orm_mode = True

