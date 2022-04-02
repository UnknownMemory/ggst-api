import unittest

from GGST.API import API
from .config import steamID, steamIDHex


class GGSTAPITests(unittest.TestCase):

    def test_login(self):
        strive: API = API()
        strive.login(steamID, steamIDHex, "pc")
        
        self.assertIsNotNone(strive.token)
        self.assertIsNotNone(strive.currentUser)


if __name__ == '__main__':
    unittest.main()