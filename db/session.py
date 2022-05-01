from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Connects to the database (Table creation call in main.py)
engine = create_engine("postgresql://postgres:admin@127.0.0.1:5432/demodb")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()