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


# Helper Functions


def admin_required(current_user):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


def librarian_required(current_user):

    if current_user.role not in [
        "admin",
        "librarian"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Librarian access required"
        )


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

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    admin_required(
        current_user
    )

    existing_user = await crud.get_user_by_email(

        db,

        user.email
    )

    if existing_user:

        raise HTTPException(

            status_code=400,

            detail="Email already exists"
        )

    if user.role not in [

        "user",

        "librarian"
    ]:

        raise HTTPException(

            status_code=400,

            detail="Role can only be user or librarian"
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

    admin_required(
        current_user
    )

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

    admin_required(
        current_user
    )

    user = await crud.get_user_by_id(

        db,

        user_id
    )

    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )

    return await crud.update_user(

        db,

        user_id,

        user_data
    )


@router.delete(
    "/users/{user_id}"
)
async def delete_user(

    user_id: int,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    admin_required(
        current_user
    )

    if user_id == current_user.id:

        raise HTTPException(

            status_code=400,

            detail="Admin cannot delete itself"
        )

    result = await crud.delete_user(

        db,

        user_id
    )

    if not result:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )

    return {

        "message":
        "User deleted successfully"
    }


# User Profile


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

    admin_required(
        current_user
    )

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

    admin_required(
        current_user
    )

    if book.total_copies <= 0:

        raise HTTPException(

            status_code=400,            



            detail="Total copies must be greater than 0"
        )

    if book.available_copies < 0:

        raise HTTPException(

            status_code=400,

            detail="Available copies cannot be negative"
        )

    if book.available_copies > book.total_copies:

        raise HTTPException(

            status_code=400,

            detail="Available copies cannot exceed total copies"
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

    skip: int = 0,

    limit: int = 5,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    return await crud.get_all_books(

        db,

        skip,

        limit
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

    admin_required(
        current_user
    )

    if (

        book_data.total_copies is not None

        and

        book_data.total_copies <= 0

    ):

        raise HTTPException(

            status_code=400,

            detail="Total copies must be greater than 0"
        )

    updated_book = await crud.update_book(

        db,

        book_id,

        book_data
    )

    if not updated_book:

        raise HTTPException(

            status_code=404,

            detail="Book not found"
        )

    return updated_book


# Issue Book


@router.post(
    "/issue-book/",
    response_model=schemas.IssuedBookResponse
)
async def issue_book(

    issue_data: schemas.IssueBookCreate,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    librarian_required(
        current_user
    )

    result = await crud.issue_book(

        db,

        issue_data
    )

    if result == "book_not_found":

        raise HTTPException(

            status_code=404,

            detail="Book not found"
        )

    if result == "user_not_found":

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )

    if result == "invalid_user":

        raise HTTPException(

            status_code=400,

            detail="Selected user is invalid"
        )

    if result == "book_already_issued":

        raise HTTPException(

            status_code=400,

            detail="User already has this book issued"
        )

    if result == "no_copy_available":

        raise HTTPException(

            status_code=400,

            detail="No copy available. User can join waitlist."
        )

    return result


# Waitlist


@router.post(
    "/waitlist/{book_id}"
)
async def join_waitlist(

    book_id: int,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    result = await crud.join_waitlist(

        db,

        book_id,

        current_user
    )

    if result == "book_not_found":

        raise HTTPException(

            status_code=404,

            detail="Book not found"
        )

    if result == "book_available":

        raise HTTPException(

            status_code=400,

            detail="Book is available. No need to join waitlist."
        )

    if result == "already_joined":

        raise HTTPException(

            status_code=400,

            detail="Already in waitlist"
        )

    if result == "only_user_allowed":

        raise HTTPException(

            status_code=403,

            detail="Only users can join waitlist"
        )

    return {

        "message": "Added to waitlist successfully"
    }


@router.get(
    "/waitlist/{book_id}",
    response_model=List[schemas.WaitlistResponse]
)
async def get_book_waitlist(

    book_id: int,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    result = await crud.get_book_waitlist(

        db,

        book_id
    )

    if result == "book_not_found":

        raise HTTPException(

            status_code=404,

            detail="Book not found"
        )

    return result


# Return Book


@router.put(
    "/return-book/",
    response_model=schemas.IssuedBookResponse
)
async def return_book(

    data: schemas.ReturnBookRequest,

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    result = await crud.return_book(

        db,

        data.book_id,

        current_user
    )

    if result == "issued_record_not_found":

        raise HTTPException(

            status_code=404,

            detail="No active issued record found"
        )

    return result


# Issued Books


@router.get(
    "/issued-books/",
    response_model=List[schemas.IssuedBookResponse]
)
async def get_issued_books(

    db: AsyncSession = Depends(get_db),

    current_user=Depends(get_current_user)

):

    librarian_required(
        current_user
    )

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

    return await crud.get_user_issued_books(

        db,

        user_id
    )