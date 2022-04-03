import msgpack
import requests
import logging
import json

from typing import Final, List, Union, Any


PLAYSTATION: Final = 1
PC: Final = 3
VERSION: Final = "0.1.1"

class API:
    def __init__(self) -> None:
        self.host = "https://ggst-game.guiltygear.com"
        self.token = None
        self.currentUser = None

    def request(self, endpoint: str, body: List) -> Union[List, None]:
        headers = {'User-Agent': 'Steam', 'Content-Type': "application/x-www-form-urlencoded", 'Cache-Control': 'no-cache'}
        url: str = self.host + endpoint 
        messagePackData = msgpack.packb(body).hex()

        try:
            res = requests.post(url, data={'data': messagePackData}, headers=headers)
        except ConnectionError as e:
            logging.exception(f"An error as occured: {e}")
            return None

        unpackedRes: List = msgpack.unpackb(res.content)
        
        return unpackedRes

    def login(self, steamID: str, steamIDHex: str, platform: str) -> Union[List, None]:
        platformID: int = 0

        if(platform.lower() == "playstation"):
            platformID = PLAYSTATION
        elif (platform.lower() == "pc"):
            platformID = PC
        else:
            logging.warning("Platform not recognized. The platform should be either 'pc' or 'playstation'.")
            return None

        data: List = [
            [
                '',
                '',
                6,
                VERSION,
                platformID
            ],
            [
                1,
                steamID,
                steamIDHex,
                256,
                ''
            ]
        ]

        res: Any = self.request("/api/user/login", data)
        self.token = res[0][0]
        self.currentUser = res[1][1][0]

        return res

    def get_rcode(self, playerID) -> List:
        data = [
            [
                self.currentUser if self.currentUser != None else "",
                self.token if self.token != None else "",
                6,
                VERSION,
                3
            ],
            [
                playerID,
                7,
                -1,
                -1,
                -1,
                -1
            ]
        ]

        res: Any = self.request("/api/statistics/get", data)

        return json.loads(res[1][1])

    # def get_total_stats(self, playerID):
    #     data = [
    #         [
    #             self.currentUser if self.currentUser != None else "",
    #             self.token if self.token != None else "",
    #             6,
    #             VERSION,
    #             3
    #         ],
    #         [
    #             playerID,
    #             1,
    #             1,
    #             -1, # Character ID
    #             -1,
    #             -1
    #         ]
    #     ]
    #     return

    # def get_skills_stats(self, playerID):
    #     data = [
    #         [
    #             self.currentUser if self.currentUser != None else "",
    #             self.token if self.token != None else "",
    #             6,
    #             VERSION,
    #             3
    #         ],
    #         [
    #             playerID,
    #             2,
    #             1,
    #             -1, # Character ID
    #             -1,
    #             -1
    #         ]
    #     ]
    #     return