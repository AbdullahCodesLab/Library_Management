from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database import Base


# users


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="member"
    )

    issued_books: Mapped[List["IssuedBook"]] = relationship(
        back_populates="user"
    )

    waitlists: Mapped[List["Waitlist"]] = relationship(
        back_populates="user"
    )


# categories


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    books: Mapped[List["Book"]] = relationship(
        back_populates="category"
    )


# books


class Book(Base):

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )

    total_copies: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    available_copies: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    category: Mapped["Category"] = relationship(
        back_populates="books"
    )

    issued_records: Mapped[List["IssuedBook"]] = relationship(
        back_populates="book"
    )

    waitlists: Mapped[List["Waitlist"]] = relationship(
        back_populates="book"
    )


# issued_books


class IssuedBook(Base):

    __tablename__ = "issued_books"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    issued_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    returned_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    issued_book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
    )

    books_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    book: Mapped["Book"] = relationship(
        back_populates="issued_records"
    )

    user: Mapped["User"] = relationship(
        back_populates="issued_books"
    )


# waitlists


class Waitlist(Base):

    __tablename__ = "waitlists"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(
        back_populates="waitlists"
    )

    book: Mapped["Book"] = relationship(
        back_populates="waitlists"
    )