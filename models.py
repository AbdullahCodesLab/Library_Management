from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    issued_books: Mapped[List["IssuedBook"]] = relationship(
        back_populates="user"
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)

    books: Mapped[List["Book"]] = relationship(
        back_populates="category"
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    is_issued: Mapped[bool] = mapped_column(Boolean, default=False)

    category: Mapped["Category"] = relationship(
        back_populates="books"
    )

    issued_records: Mapped[List["IssuedBook"]] = relationship(
        back_populates="book"
    )


class IssuedBook(Base):
    __tablename__ = "issued_books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    issued_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    returned_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    issued_book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    books_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    book: Mapped["Book"] = relationship(
        back_populates="issued_records"
    )

    user: Mapped["User"] = relationship(
        back_populates="issued_books"
    )