import  unittest

from sqlalchemy import text

from config.db import engine,db
class DbTest(unittest.TestCase):
    def setUp(self):
        self.db=db
    def test_connect(self):
        db.execute(text("SELECT 1"))