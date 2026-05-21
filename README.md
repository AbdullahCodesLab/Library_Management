# Library Management System

This is an async Library Management System API built with FastAPI, PostgreSQL, SQLAlchemy Async, AsyncPG, and Pydantic.

## Features

- Create users
- Get all users
- Get single user
- Update user
- View user profile with assigned books
- Create book categories
- Get all categories
- Create books
- Get all books
- Get a single book
- Update book
- Get books by category
- Issue book to user
- Prevent already issued book from being issued again
- Return issued book
- Get all issued book records
- Get issued books of a specific user

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy Async
- AsyncPG
- Pydantic
- Uvicorn

## Project Structure

Library_Management/

- main.py
- database.py
- models.py
- schemas.py
- crud.py
- routes.py
- requirements.txt
- .env.example
- .gitignore
- README.md


## Setup Instructions

### 1. Clone the repository

```bash
git clone your_repo_link_here
cd Library_Management
```

### 2. Create virtual environment

```bash
python3 -m venv venv
```

### 3. Activate virtual environment

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create PostgreSQL database

Open PostgreSQL shell:

```bash
sudo -u postgres psql
```

Create database:

```sql
CREATE DATABASE library_db;
```

Exit PostgreSQL:

```sql
\q
```

### 6. Create .env file

Create a `.env` file in the project root and add:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost/library_db
```

Replace `your_password` with your PostgreSQL password.



### 7. Run the project

```bash
uvicorn main:app --reload


### 8. Open Swagger Docs

Open this URL in browser:

```text
http://127.0.0.1:8000/docs
```

Recommended testing order:

1. Create categories
2. Create books
3. Create users
4. Issue a book to a user
5. Check book status
6. Try issuing the same book again
7. Check user profile
8. Return the book
9. Check book status again
10. Issue the same book again after return

