from sqlmodel import SQLModel, Field, Column, TIMESTAMP, Relationship
from typing import List, Optional
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, nullable=False),
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(TIMESTAMP, default=datetime.now)
    )

    def __repr__(self):
        return f"<User: {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, nullable=False),
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user: Optional["User"] = Relationship(back_populates="books")
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(TIMESTAMP, default=datetime.now)
    )

    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(TIMESTAMP, default=datetime.now)
    )
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(UUID(as_uuid=True), primary_key=True, nullable=False),
    )
    rating: int = Field(lt=5)
    review_text : str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")
    created_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(TIMESTAMP, default=datetime.now)
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, sa_column=Column(TIMESTAMP, default=datetime.now)
    )

    def __repr__(self):
        return f"<Review for {self.book_uid} by user {self.book_uid}>"
