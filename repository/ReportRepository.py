from entity import Report
from repository.crudEntity import CRDEntity


class ReportRepository(CRDEntity):
    model = Report