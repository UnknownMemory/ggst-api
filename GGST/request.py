import requests
import logging
import msgpack
from typing import Union


class Request:
    def __init__(self) -> None:
        self.host: str = "https://ggst-game.guiltygear.com"

    def post(self, endpoint: str, messagePack) -> Union[list, None]:

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
