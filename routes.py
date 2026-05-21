from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import get_db


router = APIRouter()


# Users

@router.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return await crud.create_user(db, user)


@router.get("/users/", response_model=List[schemas.UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_users(db)


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.email is not None:
        existing_user = await crud.get_user_by_email(db, user_data.email)

        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already registered")

    updated_user = await crud.update_user(db, user_id, user_data)

    return updated_user


@router.get("/users/{user_id}/profile", response_model=schemas.UserProfileResponse)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    profile = await crud.get_user_profile(db, user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="User not found")

    return profile


# Categories

@router.post("/categories/", response_model=schemas.CategoryResponse)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    existing_category = await crud.get_category_by_name(db, category.name)

    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    return await crud.create_category(db, category)


@router.get("/categories/", response_model=List[schemas.CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_categories(db)


# Books

@router.post("/books/", response_model=schemas.BookResponse)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    category = await crud.get_category_by_id(db, book.category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return await crud.create_book(db, book)


@router.get("/books/", response_model=List[schemas.BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_books(db)


@router.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_single_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await crud.get_book_by_id(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.get("/books/category/{category_id}", response_model=List[schemas.BookResponse])
async def get_books_by_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    category = await crud.get_category_by_id(db, category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return await crud.get_books_by_category(db, category_id)


@router.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    book = await crud.get_book_by_id(db, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_data.category_id is not None:
        category = await crud.get_category_by_id(db, book_data.category_id)

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

    updated_book = await crud.update_book(db, book_id, book_data)

    return updated_book


# Issue Books

@router.post("/issue-book/", response_model=schemas.IssuedBookResponse)
async def issue_book(
    issue_data: schemas.IssueBookCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await crud.issue_book(db, issue_data)

    if result == "book_not_found":
        raise HTTPException(status_code=404, detail="Book not found")

    if result == "user_not_found":
        raise HTTPException(status_code=404, detail="User not found")

    if result == "book_already_issued":
        raise HTTPException(status_code=400, detail="Book is already issued")

    return result


@router.put("/return-book/{issued_book_id}", response_model=schemas.IssuedBookResponse)
async def return_book(
    issued_book_id: int,
    db: AsyncSession = Depends(get_db)
):
    issued_record = await crud.return_book(db, issued_book_id)

    if not issued_record:
        raise HTTPException(
            status_code=404,
            detail="Active issued book record not found"
        )

    return issued_record


@router.get("/issued-books/", response_model=List[schemas.IssuedBookResponse])
async def get_issued_books(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_issued_books(db)


@router.get(
    "/users/{user_id}/issued-books",
    response_model=List[schemas.IssuedBookResponse]
)
async def get_user_issued_books(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await crud.get_user_issued_books(db, user_id)