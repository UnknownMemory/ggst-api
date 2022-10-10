from typing import Dict, Tuple, Union
import json
import time
import msgpack

from .constants import VERSION, CHARACTERS
from .utils import get_platform
from .request import Request


def login(account_id: str, account_id_hex: str, platform: str) -> Tuple[str, int, str]:
    platform_id: int = get_platform(platform)

    req: list = [
        [
            "",
            "",
            6,
            VERSION,
            platform_id,
        ],
        [1, account_id, account_id_hex, 256, ""],
    ]

    message_pack = msgpack.packb(req).hex()

    request: Request = Request()
    res: list = request.post("/api/user/login", message_pack)

    return res[1][1][0], platform_id, res[0][0]


class API:
    def __init__(self, player_id, platform, token=None) -> None:
        self.player_id: str = player_id
        self.platform: int = get_platform(platform) if isinstance(platform, str) else platform
        self.token: Union[str, None] = token
        self.request: Request = Request()

    # region constants getter
    def _get_character(self, character: str) -> int:
        if character in CHARACTERS:
            return CHARACTERS[character]
        raise ValueError("The character was not recognized.")

    # endregion

    def _msgpacking(self, body: list):
        req: list = []

        header: list = [
            "",
            self.token if self.token is not None else "",
            6,
            VERSION,
            self.platform,
        ]

        req.append(header)
        req.append(body)
        message_pack = msgpack.packb(req).hex()

        return message_pack

    def get_rcode(self) -> Dict:
        data = self._msgpacking([self.player_id, 7, -1, -1, -1, -1])

        res: list = self.request.post("/api/statistics/get", data)

        return json.loads(res[1][1])

    def get_matches_stats(self, character: str = "All") -> Dict:
        character_id: int = self._get_character(character)

        data = self._msgpacking([self.player_id, 1, 1, character_id, -1, -1])

        res: list = self.request.post("/api/statistics/get", data)
        return json.loads(res[1][1])

    def get_skills_stats(self, character: str = "All") -> Dict:
        character_id: int = self._get_character(character)

        data = self._msgpacking([self.player_id, 2, 1, character_id, -1, -1])

        res: list = self.request.post("/api/statistics/get", data)
        return json.loads(res[1][1])

    # region ranking methods
    def get_chara_level_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: list = self.request.post("/api/ranking/chara_level", data)
        return res[1][4]

    def get_vip_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: list = self.request.post("/api/ranking/vip", data)
        return res[1][4]

    def get_total_wins_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: list = self.request.post("/api/ranking/total_wins", data)
        return res[1][4]

    def get_survival_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: list = self.request.post("/api/ranking/survival", data)
        return res[1][4]

    def get_monthly_wins_ranking(self, page: int = 0):
        current_month: str = time.strftime("%Y%m")

        data = self._msgpacking([current_month, page, 0, -1, 0])

        res: list = self.request.post("/api/ranking/monthly_wins", data)
        return res[1][4]

    # endregion
