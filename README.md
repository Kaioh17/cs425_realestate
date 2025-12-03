# CS425 Real Estate - README

**Project Overview**
- **Purpose**: A small real-estate demo project that connects to a PostgreSQL database and provides basic user/agent queries.
- **Language**: Python
- **DB**: PostgreSQL
- **ORM**: SQLAlchemy (used via `sqlalchemy` package; raw `psycopg2` is also present in some scripts)

**Repository Structure**
- `app/` : Application code and small runner
  - `requirement.txt` : Python dependencies
  - `user.py` : Example code that queries users using SQLAlchemy `text()` statements and a session generator
  - `db/` : Database utilities
    - `connect.py` : SQLAlchemy engine, `SessionLocal`, `Base` and `get_db()` generator
    - `create_models.py` : (older style) script that uses `psycopg2` to create tables

**Quick Setup**
- Create and activate a virtual environment (recommended):

```
python -m venv venv
for linux:
  source venv/bin/activate
for windows: 
  venv\Scripts\activate.bat
```

- Install dependencies:

```
pip install -r app/requirement.txt
```

- Provide database credentials using environment variables (or a `.env` file in `app/db` or project root). The following variables are expected by `connect.py`:
  - `DB_NAME`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_HOST`
  - `DB_PORT`

Example `.env` content:

```
DB_NAME=realestate_db
DB_USER=postgres
DB_PASSWORD=secret
DB_HOST=127.0.0.1
DB_PORT=5432
```

**How to Run (basic)**
- Preferred: run as a module from the project root so package imports work correctly:

```
cd /home/kaioh/cs425_realestate
python -m app.operations.user
```

- Alternative: run the script directly but set `PYTHONPATH` so `app` is importable:

```
cd /home/kaioh/cs425_realestate
PYTHONPATH=$PWD python app/operations/user.py
```

Notes:
- Running `python app/operations/user.py` without adjusting `PYTHONPATH` will raise `ModuleNotFoundError: No module named 'app'` because Python's import path will not include the project root when executing the script directly.
- Using `python -m app.operations.user` runs the module in package context and is the recommended approach.



**SQLAlchemy - A Simple Guide**
- SQLAlchemy has two main layers:
  - **Core**: SQL expression language, `create_engine`, `text()` — good for raw SQL.
  - **ORM**: Declarative mapping with `declarative_base()` and model classes; works with `Session` to persist and query objects.

Core components you'll see in this project:
- **Engine**: created with `create_engine()`; it manages DB connections.
- **SessionLocal**: created with `sessionmaker(...)`; used to create sessions scoped to a unit of work.
- **Base**: `declarative_base()` used to define ORM models.
- **get_db()**: a generator-based helper that yields a session and ensures it is closed after use.

To create db and test data use `app/db/schema.sql` you can add more test data as needed. 

**How This Project Uses SQLAlchemy**
- `app/db/connect.py`:
  - Builds the connection string from environment variables and calls `create_engine()`.
  - Defines `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`.
  - Defines `Base = declarative_base()` for ORM models.
  - Implements `get_db()` as a generator that yields a session (intended for dependency injection or safe session handling).


