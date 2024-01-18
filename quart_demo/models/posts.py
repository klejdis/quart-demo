from sqlalchemy.orm import DeclarativeBase


class Posts(DeclarativeBase):
    id: int
    title: str
    content: str
