import msgpack
import json
import time
from typing import Dict, Tuple, Union, Any

from .constants import VERSION, CHARACTERS
from .utils import get_platform
from .request import Request


def login(accountID: str, accountIDHex: str, platform: str) -> Tuple[str, str, int]:
    platformID: int = get_platform(platform)

    req: list = [
        [
            "",
            "",
            6,
            VERSION,
            platformID,
        ],
        [1, accountID, accountIDHex, 256, ""],
    ]

    messagePack = msgpack.packb(req).hex()

    request: Request = Request()
    res: Any = request.post("/api/user/login", messagePack)

    return res[0][0], res[1][1][0], platformID


class API:
    def __init__(self, user) -> None:
        self.token: Union[str, None] = user[0]
        self.playerID: str = user[1]
        self.platform: int = get_platform(user[2]) if isinstance(user[2], str) else user[2]
        self.request: Request = Request()

    # region constants getter
    def _get_character(self, character: str) -> int:
        if character in CHARACTERS.keys():
            return CHARACTERS[character]
        else:
            raise ValueError("The character was not recognized.")

    # endregion

    def _msgpacking(self, body: list):
        req: list = []

        header: list = [
            self.playerID if self.playerID != None else "",
            self.token if self.token != None else "",
            6,
            VERSION,
            self.platform,
        ]

        req.append(header)
        req.append(body)
        messagePack = msgpack.packb(req).hex()

        return messagePack

    def get_rcode(self) -> Dict:
        data = self._msgpacking([self.playerID, 7, -1, -1, -1, -1])

        res: Any = self.request.post("/api/statistics/get", data)

        return json.loads(res[1][1])

    def get_matches_stats(self, character: str = "All") -> Dict:
        characterID: int = self._get_character(character)

        data = self._msgpacking([self.playerID, 1, 1, characterID, -1, -1])

        res: Any = self.request.post("/api/statistics/get", data)
        return json.loads(res[1][1])

    def get_skills_stats(self, character: str = "All") -> Dict:
        characterID: int = self._get_character(character)

        data = self._msgpacking([self.playerID, 2, 1, characterID, -1, -1])

        res: Any = self.request.post("/api/statistics/get", data)
        return json.loads(res[1][1])

    # region ranking methods
    def get_chara_level_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: Any = self.request.post("/api/ranking/chara_level", data)
        return res[1][4]

    def get_vip_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: Any = self.request.post("/api/ranking/vip", data)
        return res[1][4]

    def get_total_wins_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: Any = self.request.post("/api/ranking/total_wins", data)
        return res[1][4]

    def get_survival_ranking(self, page: int = 0):
        data = self._msgpacking([page, 0, -1, 0])

        res: Any = self.request.post("/api/ranking/survival", data)
        return res[1][4]

    def get_monthly_wins_ranking(self, page: int = 0):
        currentMonth: str = time.strftime("%Y%m")

        data = self._msgpacking([currentMonth, page, 0, -1, 0])

        res: Any = self.request.post("/api/ranking/monthly_wins", data)
        return res[1][4]

    # endregion
