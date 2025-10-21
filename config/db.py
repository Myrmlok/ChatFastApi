import os
from sys import exception

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config.envApp import settings
engine=create_engine(settings.CONNECTION_STRING)

local_session=sessionmaker(bind=engine)
def get_db():
    db=local_session()
    try:
        yield db
    finally:
        db.close()



class Base(DeclarativeBase):pass
def create_all_tables():
    Base.metadata.create_all(engine)

