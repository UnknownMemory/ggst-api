from optparse import OptionParser
import msgpack
import requests
import logging
import json
import time

from typing import Dict, Optional, Union, Any
from .constants import PLAYSTATION, PC, VERSION, CHARACTERS


class API:
    def __init__(self) -> None:
        self.host: str = "https://ggst-game.guiltygear.com"
        self.token: Optional[str] = None
        self.currentUser: Optional[str] = None
        self.platform: Optional[int] = None

    # region constants getter
    def _get_platform(self, platform: str) -> int:
        if platform.lower() == "playstation":
            return PLAYSTATION
        elif platform.lower() == "pc":
            return PC
        else:
            raise ValueError("Platform not recognized. The platform should be either 'pc' or 'playstation'.")

    def _get_character(self, character: str) -> int:
        if character in CHARACTERS.keys():
            return CHARACTERS[character]
        else:
            raise ValueError("The character was not recognized.")

    # endregion

    def _request(self, endpoint: str, messagePack) -> Union[list, None]:

        headers = {
            "User-Agent": "Steam",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        url: str = self.host + endpoint

        try:
            res = requests.post(url, data={"data": messagePack}, headers=headers)
        except ConnectionError as e:
            logging.exception(f"An error as occured: {e}")
            return None

        unpackedRes: list = msgpack.unpackb(res.content)

        return unpackedRes

    def _msgpacking(self, platform: int, body: list, playerID: str = ""):
        req: list = []

        header: list = [
            self.currentUser if self.currentUser != None else playerID,
            self.token if self.token != None else "",
            6,
            VERSION,
            self.platform if self.platform != None else platform,
        ]

        req.append(header)
        req.append(body)
        messagePack = msgpack.packb(req).hex()

        return messagePack

    def login(self, accountID: str, accountIDHex: str, platform: str) -> Union[list, None]:
        platformID: int = self._get_platform(platform)

        data = self._msgpacking(platformID, [1, accountID, accountIDHex, 256, ""])

        res: Any = self._request("/api/user/login", data)
        self.token = res[0][0]
        self.currentUser = res[1][1][0]
        self.platform = platformID

        return res

    def get_rcode(self, playerID: str, platform: str = "pc") -> Dict:
        platformID: int = self._get_platform(platform)

        data = self._msgpacking(platformID, [playerID, 7, -1, -1, -1, -1])

        res: Any = self._request("/api/statistics/get", data)

        return json.loads(res[1][1])

    def get_matches_stats(self, playerID: str, character: str = "All", platform: str = "pc") -> Dict:
        platformID: int = self._get_platform(platform)
        characterID: int = self._get_character(character)

        data = self._msgpacking(platformID, [playerID, 1, 1, characterID, -1, -1])

        res: Any = self._request("/api/statistics/get", data)
        return json.loads(res[1][1])

    def get_skills_stats(self, playerID: str, character: str = "All", platform: str = "pc") -> Dict:
        platformID: int = self._get_platform(platform)
        characterID: int = self._get_character(character)

        data = self._msgpacking(platformID, [playerID, 2, 1, characterID, -1, -1])

        res: Any = self._request("/api/statistics/get", data)
        return json.loads(res[1][1])

    def get_chara_level_ranking(self, playerID: str, page: int = 0, platform: str = "pc"):
        platformID: int = self._get_platform(platform)

        data = self._msgpacking(platformID, [page, 0, -1, 0], playerID)

        res: Any = self._request("/api/ranking/chara_level", data)
        return res[1][4]

    def get_vip_ranking(self, playerID: str, page: int = 0, platform: str = "pc"):
        platformID: int = self._get_platform(platform)

        data = self._msgpacking(platformID, [page, 0, -1, 0], playerID)

        res: Any = self._request("/api/ranking/vip", data)
        return res[1][4]

    def get_total_wins_ranking(self, playerID: str, page: int = 0, platform: str = "pc"):
        platformID: int = self._get_platform(platform)

        data = self._msgpacking(platformID, [page, 0, -1, 0], playerID)

        res: Any = self._request("/api/ranking/total_wins", data)
        return res[1][4]

    def get_survival_ranking(self, playerID: str, page: int = 0, platform: str = "pc"):
        platformID: int = self._get_platform(platform)

        data = self._msgpacking(platformID, [page, 0, -1, 0], playerID)

        res: Any = self._request("/api/ranking/survival", data)
        return res[1][4]

    def get_monthly_wins_ranking(self, playerID: str, page: int = 0, platform: str = "pc"):
        platformID: int = self._get_platform(platform)
        currentMonth: str = time.strftime("%Y%m")

        data = self._msgpacking(platformID, [currentMonth, page, 0, -1, 0], playerID)

        res: Any = self._request("/api/ranking/monthly_wins", data)
        return res[1][4]
