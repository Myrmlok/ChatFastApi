from entity import MessageEntity
from repository.crudEntity import CRDEntity


class MessageRepository(CRDEntity):
    model=MessageEntity