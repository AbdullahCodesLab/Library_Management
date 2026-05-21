from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# User Schemas


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True



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


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    name: str
    category_id: int
    is_issued: bool

    class Config:
        from_attributes = True


# Issued Book Schemas

class IssueBookCreate(BaseModel):
    issued_book_id: int
    books_user_id: int


class IssuedBookResponse(BaseModel):
    id: int
    issued_time: datetime
    returned_time: Optional[datetime] = None
    issued_book_id: int
    books_user_id: int

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
    issued_books: List[UserIssuedBookInfo]