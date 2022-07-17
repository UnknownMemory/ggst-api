import unittest

import GGST
from .config import steamID, steamIDHex, striveID


class GGSTAPITests(unittest.TestCase):
    def test_login(self):
        user: GGST.login = GGST.login(steamID, steamIDHex, "pc")
        strive: GGST.API = GGST.API(user)
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

    def test_get_vip_ranking(self):
        strive: API = API()
        vipRanking = strive.get_vip_ranking(striveID)
        self.assertEqual(len(vipRanking), 20)

    def test_total_wins_ranking(self):
        strive: API = API()
        winsRanking = strive.get_total_wins_ranking(striveID)
        self.assertEqual(len(winsRanking), 20)

    def test_chara_level_ranking(self):
        strive: API = API()
        charaRanking = strive.get_chara_level_ranking(striveID)
        self.assertEqual(len(charaRanking), 20)

    def test_survival_ranking(self):
        strive: API = API()
        survivalRanking = strive.get_survival_ranking(striveID)
        self.assertEqual(len(survivalRanking), 20)

    def test_monthly_wins_ranking(self):
        strive: API = API()
        monthlyRanking = strive.get_monthly_wins_ranking(striveID)
        self.assertEqual(len(monthlyRanking), 20)


if __name__ == "__main__":
    unittest.main()
