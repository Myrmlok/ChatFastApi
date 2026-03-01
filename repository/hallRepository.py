from typing import List

from sqlalchemy.ext.asyncio import AsyncSession


from entity import Hall, Vertex
from repository.crudEntity import CRDEntity
from sqlalchemy import select

class HallRepository(CRDEntity):
    model=Hall