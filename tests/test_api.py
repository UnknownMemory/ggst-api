import unittest

from GGST.API import API
from .config import steamID, steamIDHex, striveID


class GGSTAPITests(unittest.TestCase):

    def test_login(self):
        strive: API = API()
        strive.login(steamID, steamIDHex, "pc")
        self.assertIsNotNone(strive.token)
        self.assertIsNotNone(strive.currentUser)

    def test_get_rcode(self):
        strive: API = API()
        rCode = strive.get_rcode(striveID)
        self.assertIn("Update_Year", rCode.keys())
    
    def test_get_total_stats(self):
        strive: API = API()
        totalStats = strive.get_total_stats(striveID)
        self.assertIn("HighRound", totalStats.keys())

if __name__ == '__main__':
    unittest.main()