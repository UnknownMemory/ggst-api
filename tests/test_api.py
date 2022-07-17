from typing import Tuple
import unittest

import GGST
from .config import steamID, steamIDHex, striveID


class GGSTAPITests(unittest.TestCase):
    def test_login(self):
        user: Tuple = GGST.login(steamID, steamIDHex, "pc")
        strive: GGST.API = GGST.API(user)
        self.assertIsNotNone(strive.token)
        self.assertIsNotNone(strive.playerID)

    def test_get_rcode(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        rCode = strive.get_rcode()
        self.assertIn("Update_Year", rCode.keys())

    def test_get_matches_stats(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        totalStats = strive.get_matches_stats()
        self.assertIn("HighRound", totalStats.keys())

    def test_get_skills_stats(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        skillStats = strive.get_skills_stats()
        self.assertIn("BRScore_Attack", skillStats.keys())

    def test_get_vip_ranking(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        vipRanking = strive.get_vip_ranking()
        self.assertEqual(len(vipRanking), 20)

    def test_total_wins_ranking(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        winsRanking = strive.get_total_wins_ranking()
        self.assertEqual(len(winsRanking), 20)

    def test_chara_level_ranking(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        charaRanking = strive.get_chara_level_ranking()
        self.assertEqual(len(charaRanking), 20)

    def test_survival_ranking(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        survivalRanking = strive.get_survival_ranking()
        self.assertEqual(len(survivalRanking), 20)

    def test_monthly_wins_ranking(self):
        strive: GGST.API = GGST.API((None, striveID, "pc"))
        monthlyRanking = strive.get_monthly_wins_ranking()
        self.assertEqual(len(monthlyRanking), 20)


if __name__ == "__main__":
    unittest.main()
