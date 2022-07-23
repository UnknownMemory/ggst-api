import unittest

import GGST
from .config import STEAM_ID, STEAM_ID_HEX, STRIVE_ID


class GGSTAPITests(unittest.TestCase):
    def test_login(self):
        player_id: str
        platform: int
        token: str

        player_id, platform, token = GGST.login(STEAM_ID, STEAM_ID_HEX, "pc")
        strive: GGST.API = GGST.API(player_id, platform, token)
        self.assertIsNotNone(strive.token)
        self.assertIsNotNone(strive.player_id)

    def test_get_rcode(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        rcode = strive.get_rcode()
        self.assertIn("Update_Year", rcode.keys())

    def test_get_matches_stats(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        total_stats = strive.get_matches_stats()
        self.assertIn("HighRound", total_stats.keys())

    def test_get_skills_stats(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        skill_stats = strive.get_skills_stats()
        self.assertIn("BRScore_Attack", skill_stats.keys())

    def test_get_vip_ranking(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        vip_ranking = strive.get_vip_ranking()
        self.assertEqual(len(vip_ranking), 20)

    def test_total_wins_ranking(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        wins_ranking = strive.get_total_wins_ranking()
        self.assertEqual(len(wins_ranking), 20)

    def test_chara_level_ranking(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        chara_ranking = strive.get_chara_level_ranking()
        self.assertEqual(len(chara_ranking), 20)

    def test_survival_ranking(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        survival_ranking = strive.get_survival_ranking()
        self.assertEqual(len(survival_ranking), 20)

    def test_monthly_wins_ranking(self):
        strive: GGST.API = GGST.API(STRIVE_ID, "pc")
        monthly_ranking = strive.get_monthly_wins_ranking()
        self.assertEqual(len(monthly_ranking), 20)


if __name__ == "__main__":
    unittest.main()
