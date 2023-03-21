import unittest

import GGST
from .config import STEAM_USERNAME, STEAM_PASSWORD


class GGSTAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.strive: GGST.API = GGST.API()
        cls.strive.login(STEAM_USERNAME, STEAM_PASSWORD)

    def test_login(self):
        self.assertIsNotNone(self.strive.token)
        self.assertIsNotNone(self.strive.player_id)

    def test_get_rcode(self):
        rcode = self.strive.get_rcode()
        self.assertIn("Update_Year", rcode.keys())

    def test_get_matches_stats(self):
        total_stats = self.strive.get_matches_stats()
        self.assertIn("HighRound", total_stats.keys())

    def test_get_skills_stats(self):
        skill_stats = self.strive.get_skills_stats()
        self.assertIn("BRScore_Attack", skill_stats.keys())
    #
    # def test_get_vip_ranking(self):
    #     vip_ranking = self.strive.get_vip_ranking()
    #     self.assertEqual(len(vip_ranking), 20)

    # def test_total_wins_ranking(self):
    #     wins_ranking = self.strive.get_total_wins_ranking()
    #     self.assertEqual(len(wins_ranking), 20)

    # def test_chara_level_ranking(self):
    #     chara_ranking = self.strive.get_chara_level_ranking()
    #     self.assertEqual(len(chara_ranking), 20)
    #
    # def test_survival_ranking(self):
    #     survival_ranking = self.strive.get_survival_ranking()
    #     self.assertEqual(len(survival_ranking), 20)
    #
    # def test_monthly_wins_ranking(self):
    #     monthly_ranking = self.strive.get_monthly_wins_ranking()
    #     self.assertEqual(len(monthly_ranking), 20)


if __name__ == "__main__":
    unittest.main()
