from config.base import Base
from entity import FocusPoint
from repository.crudEntity import CRDEntity


class FocusPointRepository(CRDEntity):
    model = FocusPoint