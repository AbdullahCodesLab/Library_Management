from pydantic import BaseModel, EmailStr

from datetime import datetime

from typing import Optional, List


# User Schemas


class UserBase(BaseModel):

    name: str

    email: EmailStr

    phone_number: str


class UserCreate(UserBase):

    password: str

    role: str


class UserUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None

    phone_number: Optional[str] = None

    role: Optional[str] = None


class UserResponse(UserBase):

    id: int

    role: str

    class Config:

        from_attributes = True


# JWT Schemas


class Token(BaseModel):

    access_token: str

    token_type: str


# Category Schemas


class CategoryBase(BaseModel):

    name: str


class CategoryCreate(CategoryBase):

    pass


class CategoryResponse(CategoryBase):

    id: int

    class Config:

        from_attributes = True


# Book Schemas


class BookBase(BaseModel):

    name: str

    category_id: int

    total_copies: int

    available_copies: int


class BookCreate(BookBase):

    pass


class BookUpdate(BaseModel):

    name: Optional[str] = None

    category_id: Optional[int] = None

    total_copies: Optional[int] = None

    available_copies: Optional[int] = None


class BookResponse(BaseModel):

    id: int

    name: str

    category_id: int

    total_copies: int

    available_copies: int

    class Config:

        from_attributes = True


# Issue Book Schemas


class IssueBookCreate(BaseModel):

    issued_book_id: int

    user_id: int


# Return Book Schema


class ReturnBookRequest(BaseModel):

    book_id: int


# Issued Book Response


class IssuedBookResponse(BaseModel):

    id: int

    issued_time: datetime

    returned_time: Optional[datetime] = None

    issued_book_id: int

    books_user_id: int

    class Config:

        from_attributes = True


# Waitlist Schemas


class WaitlistCreate(BaseModel):

    book_id: int


class WaitlistResponse(BaseModel):

    id: int

    user_id: int

    book_id: int

    created_at: datetime

    class Config:

        from_attributes = True


# User Profile Schemas


class UserIssuedBookInfo(BaseModel):

    book_id: int

    book_name: str

    category_name: str

    issued_time: datetime

    returned_time: Optional[datetime] = None

    status: str


class UserProfileResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone_number: str

    role: str

    issued_books: List[UserIssuedBookInfo]