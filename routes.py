from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas

from auth import create_access_token
from oauth2 import get_current_user
from database import get_db


router = APIRouter()


# Login

@router.post(
    "/login",
    response_model=schemas.Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    authenticated_user = await crud.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not authenticated_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": authenticated_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Users

@router.post(
    "/users/",
    response_model=schemas.UserResponse
)
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):

    existing_user = await crud.get_user_by_email(
        db,
        user.email
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return await crud.create_user(
        db,
        user
    )


@router.get(
    "/users/",
    response_model=List[schemas.UserResponse]
)
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return await crud.get_all_users(
        db
    )


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = await crud.get_user_by_id(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put(
    "/users/{user_id}",
    response_model=schemas.UserResponse
)
async def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = await crud.get_user_by_id(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_data.email is not None:

        existing_user = await crud.get_user_by_email(
            db,
            user_data.email
        )

        if existing_user and existing_user.id != user_id:

            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

    updated_user = await crud.update_user(
        db,
        user_id,
        user_data
    )

    return updated_user


@router.get(
    "/users/{user_id}/profile",
    response_model=schemas.UserProfileResponse
)
async def get_user_profile(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    profile = await crud.get_user_profile(
        db,
        user_id
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return profile


# Categories

@router.post(
    "/categories/",
    response_model=schemas.CategoryResponse
)
async def create_category(
    category: schemas.CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_category = await crud.get_category_by_name(
        db,
        category.name
    )

    if existing_category:

        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )

    return await crud.create_category(
        db,
        category
    )


@router.get(
    "/categories/",
    response_model=List[schemas.CategoryResponse]
)
async def get_categories(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return await crud.get_all_categories(
        db
    )


# Books

@router.post(
    "/books/",
    response_model=schemas.BookResponse
)
async def create_book(
    book: schemas.BookCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    category = await crud.get_category_by_id(
        db,
        book.category_id
    )

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return await crud.create_book(
        db,
        book
    )


@router.get(
    "/books/",
    response_model=List[schemas.BookResponse]
)
async def get_books(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return await crud.get_all_books(
        db
    )


@router.get(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
async def get_single_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    book = await crud.get_book_by_id(
        db,
        book_id
    )

    if not book:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@router.get(
    "/books/category/{category_id}",
    response_model=List[schemas.BookResponse]
)
async def get_books_by_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    category = await crud.get_category_by_id(
        db,
        category_id
    )

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return await crud.get_books_by_category(
        db,
        category_id
    )


@router.put(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
async def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    book = await crud.get_book_by_id(
        db,
        book_id
    )

    if not book:

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if book_data.category_id is not None:

        category = await crud.get_category_by_id(
            db,
            book_data.category_id
        )

        if not category:

            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    updated_book = await crud.update_book(
        db,
        book_id,
        book_data
    )

    return updated_book


# Issue Books

@router.post(
    "/issue-book/",
    response_model=schemas.IssuedBookResponse
)
async def issue_book(
    issue_data: schemas.IssueBookCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = await crud.issue_book(
        db,
        issue_data,
        current_user
    )

    if result == "book_not_found":

        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if result == "book_already_issued":

        raise HTTPException(
            status_code=400,
            detail="Book is already issued"
        )

    return result


@router.put(
    "/return-book/{issued_book_id}",
    response_model=schemas.IssuedBookResponse
)
async def return_book(
    issued_book_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    result = await crud.return_book(
        db,
        issued_book_id,
        current_user
    )

    if result == "issued_record_not_found":

        raise HTTPException(
            status_code=404,
            detail="Active issued book record not found"
        )

    if result == "not_your_book":

        raise HTTPException(
            status_code=403,
            detail="You can only return your own books"
        )

    return result


@router.get(
    "/issued-books/",
    response_model=List[schemas.IssuedBookResponse]
)
async def get_issued_books(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return await crud.get_all_issued_books(
        db
    )


@router.get(
    "/users/{user_id}/issued-books",
    response_model=List[schemas.IssuedBookResponse]
)
async def get_user_issued_books(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = await crud.get_user_by_id(
        db,
        user_id
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return await crud.get_user_issued_books(
        db,
        user_id
    )