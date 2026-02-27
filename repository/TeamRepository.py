from sqlalchemy.ext.asyncio import AsyncSession

from entity import Team
from repository.crudEntity import CRDEntity


class TeamRepository(CRDEntity):
    model = Team