import unittest

from GGST import API
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
    
    def test_get_matches_stats(self):
        strive: API = API()
        totalStats = strive.get_matches_stats(striveID)
        self.assertIn("HighRound", totalStats.keys())

    def test_get_skills_stats(self):
        strive: API = API()
        skillStats = strive.get_skills_stats(striveID)
        self.assertIn("BRScore_Attack", skillStats.keys())

if __name__ == '__main__':
    unittest.main()