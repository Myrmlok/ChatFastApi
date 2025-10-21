import unittest
from security.services.jwtService import create_access_token
class TestJwt(unittest.TestCase):
    def test_generate(self):
        print(create_access_token({"uuid":1}))
