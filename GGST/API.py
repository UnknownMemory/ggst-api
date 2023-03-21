from typing import Dict, Tuple, Union
import json
import time

from .constants import VERSION, CHARACTERS
from .crypt import encrypt_request_data
from .steam import steam_login
from .utils import get_platform
from .request import Request


class API:
    def __init__(self, player_id: str = None, platform: str = None, token: str = None) -> None:
        self.steam_id: str = None
        self.steam_id_hex: str = None
        self.player_id: str = player_id
        self.platform: int = get_platform(platform) if isinstance(platform, str) else platform
        self.token: Union[str, None] = token
        self.request: Request = Request()


    def _get_character(self, character: str) -> int:
        if character in CHARACTERS:
            return CHARACTERS[character]
        raise ValueError("The character was not recognized.")

    def _msgpacking(self, body: list):
        req: list = []

        header: list = [
            self.player_id if self.player_id is not None else "",
            self.token,
            2,
            VERSION,
            self.platform,
        ]

        req.append(header)
        req.append(body)
        message_pack = encrypt_request_data(req)

        return message_pack

    def login(self, user: str, password: str, auth=None, padding=0) -> Tuple[str, int, str]:
        platform_id: int = get_platform("pc")
        if not auth:
            auth = steam_login(user, password)

        self.steam_id = auth['id']
        self.steam_id_hex = hex(self.steam_id)[:2]

        req: list = [
            [
                "",
                "",
                2,
                VERSION,
                platform_id,
            ],
            [
                1,
                self.steam_id,
                self.steam_id_hex,
                256,
                auth["token"]
            ],
        ]

        message_pack = encrypt_request_data(req)

        request: Request = Request()

        try:
            res: list = request.post("user/login", message_pack if padding >= 0 else message_pack[:padding])
        except Exception as e:
            return self.login(user, password, auth, padding - 2)

        self.player_id = res[1][1][0]
        self.token = res[0][0]
        self.platform = platform_id
        return

    def get_rcode(self) -> Dict:
        data = self._msgpacking([self.player_id, 7, -1, -1, -1, -1])

        res: list = self.request.post("statistics/get", data)
        return json.loads(res[1][1])

    def get_matches_stats(self, character: str = "All") -> Dict:
        character_id: int = self._get_character(character)

        data = self._msgpacking([self.player_id, 1, 1, character_id, -1, -1])

        res: list = self.request.post("statistics/get", data)
        return json.loads(res[1][1])

    def get_skills_stats(self, character: str = "All") -> Dict:
        character_id: int = self._get_character(character)

        data = self._msgpacking([self.player_id, 2, 1, character_id, -1, -1])

        res: list = self.request.post("statistics/get", data)
        return json.loads(res[1][1])

    # def get_chara_level_ranking(self, page: int = 0):
    #     data = self._msgpacking([page, 0, -1, 0])
    #
    #     res: list = self.request.post("ranking/chara_level", data)
    #     return res[1][4]
    #
    # def get_vip_ranking(self, page: int = 0):
    #     data = self._msgpacking([page, 0, -1, 0])
    #
    #     res: list = self.request.post("ranking/vip", data)
    #     return res[1][4]
    #
    # def get_total_wins_ranking(self, page: int = 0):
    #     data = self._msgpacking([page, 0, -1, 0])
    #
    #     res: list = self.request.post("ranking/total_wins", data)
    #     return res[1][4]
    #
    # def get_survival_ranking(self, page: int = 0):
    #     data = self._msgpacking([page, 0, -1, 0])
    #
    #     res: list = self.request.post("ranking/survival", data)
    #     return res[1][4]
    #
    # def get_monthly_wins_ranking(self, page: int = 0):
    #     current_month: str = time.strftime("%Y%m")
    #
    #     data = self._msgpacking([current_month, page, 0, -1, 0])
    #
    #     res: list = self.request.post("ranking/monthly_wins", data)
    #     return res[1][4]
