from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from typing import Annotated
from sqlalchemy import Integer, Identity
from sqlalchemy.orm import mapped_column

class Base(AsyncAttrs,DeclarativeBase):
    __abstract__ = True
    pass
idEntity=Annotated[int,mapped_column(Integer, primary_key=True, server_default=Identity())]