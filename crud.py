from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select

from datetime import datetime

import models

import schemas

from auth import (
    hash_password,
    verify_password
)


# User CRUD


async def get_user_by_email(
    db: AsyncSession,
    email: str
):

    result = await db.execute(
        select(models.User).where(
            models.User.email == email
        )
    )

    return result.scalar_one_or_none()


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str
):

    user = await get_user_by_email(
        db,
        email
    )

    if not user:

        return None

    if not verify_password(
        password,
        user.password
    ):

        return None

    return user


async def create_user(
    db: AsyncSession,
    user: schemas.UserCreate
):

    hashed_password = hash_password(
        user.password
    )

    db_user = models.User(

        name=user.name,

        email=user.email,

        phone_number=user.phone_number,

        password=hashed_password,

        role=user.role
    )

    db.add(
        db_user
    )

    await db.commit()

    await db.refresh(
        db_user
    )

    return db_user


async def get_all_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 5
):

    result = await db.execute(

        select(models.User)

        .order_by(

            models.User.id
        )

        .offset(skip)

        .limit(limit)
    )

    return result.scalars().all()


async def get_user_by_id(
    db: AsyncSession,
    user_id: int
):

    result = await db.execute(
        select(models.User).where(
            models.User.id == user_id
        )
    )

    return result.scalar_one_or_none()


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: schemas.UserUpdate
):

    user = await get_user_by_id(
        db,
        user_id
    )

    if not user:

        return None

    if user_data.name is not None:

        user.name = user_data.name

    if user_data.email is not None:

        user.email = user_data.email

    if user_data.phone_number is not None:

        user.phone_number = user_data.phone_number

    if user_data.role is not None:

        user.role = user_data.role

    await db.commit()

    await db.refresh(
        user
    )

    return user


async def delete_user(
    db: AsyncSession,
    user_id: int
):

    user = await get_user_by_id(
        db,
        user_id
    )

    if not user:

        return None

    await db.delete(
        user
    )

    await db.commit()

    return True


# Category CRUD


async def get_category_by_name(
    db: AsyncSession,
    name: str
):

    result = await db.execute(

        select(models.Category).where(

            models.Category.name == name
        )
    )

    return result.scalar_one_or_none()


async def create_category(
    db: AsyncSession,
    category: schemas.CategoryCreate
):

    db_category = models.Category(

        name=category.name
    )

    db.add(
        db_category
    )

    await db.commit()

    await db.refresh(
        db_category
    )

    return db_category


async def get_all_categories(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 5
):

    result = await db.execute(

        select(models.Category)

        .order_by(

            models.Category.id
        )

        .offset(skip)

        .limit(limit)
    )

    return result.scalars().all()


async def get_category_by_id(
    db: AsyncSession,
    category_id: int
):

    result = await db.execute(

        select(models.Category).where(

            models.Category.id == category_id
        )
    )

    return result.scalar_one_or_none()


# Book CRUD


async def create_book(
    db: AsyncSession,
    book: schemas.BookCreate
):

    db_book = models.Book(

        name=book.name,

        category_id=book.category_id,

        total_copies=book.total_copies,

        available_copies=book.available_copies
    )

    db.add(
        db_book
    )

    await db.commit()

    await db.refresh(
        db_book
    )

    return db_book



async def get_all_books(

    db: AsyncSession,

    skip: int = 0,

    limit: int = 5
):

    result = await db.execute(

        select(models.Book)

        .order_by(

            models.Book.id
        )

        .offset(skip)

        .limit(limit)
    )

    return result.scalars().all()


async def get_book_by_id(
    db: AsyncSession,
    book_id: int
):

    result = await db.execute(

        select(models.Book).where(

            models.Book.id == book_id
        )
    )

    return result.scalar_one_or_none()


async def update_book(
    db: AsyncSession,
    book_id: int,
    book_data: schemas.BookUpdate
):

    book = await get_book_by_id(
        db,
        book_id
    )

    if not book:

        return None

    if book_data.name is not None:

        book.name = book_data.name

    if book_data.category_id is not None:

        book.category_id = book_data.category_id

    if book_data.total_copies is not None:

        book.total_copies = book_data.total_copies

    if book_data.available_copies is not None:

        book.available_copies = book_data.available_copies

    await db.commit()

    await db.refresh(
        book
    )

    return book


async def delete_book(
    db: AsyncSession,
    book_id: int
):

    book = await get_book_by_id(
        db,
        book_id
    )

    if not book:

        return None

    await db.delete(
        book
    )

    await db.commit()

    return True


# Waitlist


async def join_waitlist(
    db: AsyncSession,
    book_id: int,
    current_user
):

    book = await get_book_by_id(
        db,
        book_id
    )

    if not book:

        return "book_not_found"

    if book.available_copies > 0:

        return "book_available"

    if current_user.role != "user":

        return "only_user_allowed"

    existing = await db.execute(

        select(models.Waitlist).where(

            models.Waitlist.book_id == book_id,

            models.Waitlist.user_id == current_user.id
        )
    )

    existing = existing.scalar_one_or_none()

    if existing:

        return "already_joined"

    waitlist = models.Waitlist(

        user_id=current_user.id,

        book_id=book_id
    )

    db.add(
        waitlist
    )

    await db.commit()

    await db.refresh(
        waitlist
    )

    return waitlist


async def get_book_waitlist(
    db: AsyncSession,
    book_id: int,
    skip: int = 0,
    limit: int = 5
):

    book = await get_book_by_id(
        db,
        book_id
    )

    if not book:

        return "book_not_found"

    result = await db.execute(

        select(models.Waitlist)

        .where(

            models.Waitlist.book_id
            == book_id
        )

        .order_by(

            models.Waitlist.created_at
        )

        .offset(skip)

        .limit(limit)
    )

    return result.scalars().all()


# Issue Book


async def issue_book(
    db: AsyncSession,
    issue_data: schemas.IssueBookCreate
):

    book = await get_book_by_id(
        db,
        issue_data.issued_book_id
    )

    if not book:

        return "book_not_found"

    user = await get_user_by_id(
        db,
        issue_data.user_id
    )

    if not user:

        return "user_not_found"

    if user.role != "user":

        return "invalid_user"

    existing_issue = await db.execute(

        select(models.IssuedBook).where(

            models.IssuedBook.issued_book_id
            == issue_data.issued_book_id,

            models.IssuedBook.books_user_id
            == issue_data.user_id,

            models.IssuedBook.returned_time.is_(None)
        )
    )

    existing_issue = existing_issue.scalar_one_or_none()

    if existing_issue:

        return "book_already_issued"

    if book.available_copies <= 0:

        return "no_copy_available"

    issued_record = models.IssuedBook(

        issued_book_id=issue_data.issued_book_id,

        books_user_id=issue_data.user_id
    )

    book.available_copies -= 1

    db.add(
        issued_record
    )

    await db.commit()

    await db.refresh(
        issued_record
    )

    return issued_record

# Return Book


async def return_book(
    db: AsyncSession,
    book_id: int,
    current_user
):

    result = await db.execute(

        select(models.IssuedBook)

        .where(

            models.IssuedBook.issued_book_id == book_id,

            models.IssuedBook.books_user_id == current_user.id,

            models.IssuedBook.returned_time.is_(None)
        )
    )

    issued_record = result.scalar_one_or_none()

    if not issued_record:

        return "issued_record_not_found"

    book = await get_book_by_id(

        db,

        book_id
    )

    issued_record.returned_time = datetime.utcnow()

    if book:

        waitlist_result = await db.execute(

            select(models.Waitlist)

            .where(

                models.Waitlist.book_id == book.id
            )

            .order_by(

                models.Waitlist.created_at
            )
        )

        next_user = waitlist_result.scalars().first()

        if next_user:

            auto_issue = models.IssuedBook(

                issued_book_id=book.id,

                books_user_id=next_user.user_id
            )

            db.add(
                auto_issue
            )

            await db.delete(
                next_user
            )

        else:

            book.available_copies += 1

    await db.commit()

    await db.refresh(
        issued_record
    )

    return issued_record


# Issued Books


# Issued Books


async def get_all_issued_books(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 5
):

    result = await db.execute(

        select(models.IssuedBook)

        .order_by(

            models.IssuedBook.id
        )

        .offset(skip)

        .limit(limit)
    )

    return result.scalars().all()


async def get_user_issued_books(
    db: AsyncSession,
    user_id: int
):

    result = await db.execute(

        select(models.IssuedBook).where(

            models.IssuedBook.books_user_id
            == user_id
        )
    )

    return result.scalars().all()


# User Profile


async def get_user_profile(
    db: AsyncSession,
    user_id: int
):

    user = await get_user_by_id(
        db,
        user_id
    )

    if not user:

        return None

    result = await db.execute(

        select(
            models.IssuedBook,
            models.Book,
            models.Category
        )

        .join(
            models.Book,

            models.IssuedBook.issued_book_id
            == models.Book.id
        )

        .join(
            models.Category,

            models.Book.category_id
            == models.Category.id
        )

        .where(
            models.IssuedBook.books_user_id
            == user_id
        )
    )

    records = result.all()

    issued_books_list = []

    for issued_record, book, category in records:

        status = (

            "returned"

            if issued_record.returned_time

            else "currently issued"
        )

        issued_books_list.append(

            {

                "book_id": book.id,

                "book_name": book.name,

                "category_name": category.name,

                "issued_time": issued_record.issued_time,

                "returned_time": issued_record.returned_time,

                "status": status
            }
        )

    return {

        "id": user.id,

        "name": user.name,

        "email": user.email,

        "phone_number": user.phone_number,

        "role": user.role,

        "issued_books": issued_books_list
    }