from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

###to connect to the database(fill in the necessary slots ):
load_dotenv()
_db_name =  os.getenv("DB_NAME")
_db_password =  os.getenv("DB_PASSWORD")
_db_port =  os.getenv("DB_PORT")
_db_host =  os.getenv("DB_HOST")
_db_user=  os.getenv("DB_USER")
###SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>:<db_port>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{_db_user}:{_db_password}@{_db_host}:{_db_port}/{_db_name}'
# DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) ## we use this to connect to the database 

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

def get_db():#we create a dependency to create sesssion every time the fuction is called
    print('connection started ')
    db = SessionLocal()
    try:
        print('connection successfull')
        yield db
    finally: 
        db.close()

# connect_db().close_db()
        