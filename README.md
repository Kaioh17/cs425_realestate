# CS425 Real Estate - README
**Project Overview**

- **Purpose**: A small real-estate demo project that connects to a PostgreSQL database and provides basic user/agent queries.
- **Language**: Python
- **DB**: PostgreSQL
- **ORM**: SQLAlchemy (used via `sqlalchemy` package; raw `psycopg2` is also present in some scripts)

## Repository Structure
- `app/` : Application code and small runner
  - `requirement.txt` : Python dependencies
  - `user.py` : Example code that queries users using SQLAlchemy `text()` statements and a session generator
  - `db/` : Database utilities
    - `connect.py` : SQLAlchemy engine, `SessionLocal`, `Base` and `get_db()` generator
    - `create_models.py` : (older style) script that uses `psycopg2` to create tables

## Quick Setup

### Prerequisites
- Python 3.10 or higher from [python.org](https://www.python.org/)

### Virtual Environment
```bash
python -m venv venv
```

**Activate on Linux/macOS:**
```bash
source venv/bin/activate
```

**Activate on Windows:**
```bash
venv\Scripts\activate.bat
```

### Install Dependencies

**Linux/macOS:**
```bash
pip install -r app/requirement.txt
```

**Windows:**
```bash
pip install -r app\requirement.txt
```

## Database Setup

### Environment Variables
Set database credentials via environment variables or `.env` file in `app/db` or project root:

```env
DB_NAME=realestate_db
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Initialize Database
```bash
psql -U postgres -h localhost
```

Run these scripts in order:
1. `app/db/schema.sql` - Create tables
2. `app/db/triggers.sql` - Set up triggers and functions
3. `app/db/mock_inserts.sql` - Add test data (optional)

## How to Run

### Recommended: Run as a Module

**Linux/macOS:**
```bash
cd /home/kaioh/cs425_realestate
python -m app.operations.user
```

**Windows:**
```bash
cd path\to\cs425_realestate
python -m app.operations.user
```

### Alternative: Set PYTHONPATH

**Linux/macOS:**
```bash
cd /home/kaioh/cs425_realestate
PYTHONPATH=$PWD python app/operations/user.py
```

**Windows:**
```bash
cd path\to\cs425_realestate
set PYTHONPATH=%cd%
python app\operations\user.py
```

> **Note:** Running `python app/operations/user.py` without `PYTHONPATH` raises `ModuleNotFoundError: No module named 'app'`. Use `python -m` for package context.

## SQLAlchemy Overview

SQLAlchemy has two main layers:
- **Core**: SQL expression language, `create_engine()`, `text()` — good for raw SQL
- **ORM**: Declarative mapping with `declarative_base()` and model classes

### Key Components
- **Engine**: Manages database connections via `create_engine()`
- **SessionLocal**: Created with `sessionmaker()`; manages session lifecycle
- **Base**: `declarative_base()` for defining ORM models
- **get_db()**: Generator that yields a session and ensures cleanup

### Project Implementation
`app/db/connect.py`:
- Builds connection string from environment variables
- Creates `SessionLocal` with `sessionmaker(autocommit=False, autoflush=False, bind=engine)`
- Defines `Base = declarative_base()` for ORM models
- Implements `get_db()` as a generator for safe session handling

## Git Workflow

### 1. Start with Latest Code
```bash
git checkout main
git pull origin main
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```
For more info on see ```https://www.geeksforgeeks.org/git/introduction-to-git-branch/```

### 3. Make Changes and Commit
```bash
git add .
git commit -m "Descriptive commit message"
```

### 4. Stay Updated with Main

**Option A - Merge:**
```bash
git fetch origin
git merge origin/main
```

**Option B - Rebase (cleaner history):**
```bash
git fetch origin
git rebase origin/main
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Open a Pull Request on GitHub for review.

### 6. After Merge, Clean Up
```bash
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

### Conflict Prevention
- Pull/rebase main frequently
- Commit small, logical changes
- Communicate when editing shared files
