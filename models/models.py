from sqlalchemy import Column, Integer, String
from db.session import Base

#Used as a schema to create table (Table creation call in main.py)
class Profile(Base):
    __tablename__ = "demotable"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    age = Column(String)

class Profile2(Base):
    __tablename__ = "demotable2"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String)
    age = Column(String)