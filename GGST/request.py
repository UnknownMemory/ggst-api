from typing import Union
import logging
import requests
import msgpack


class Request:
    def __init__(self) -> None:
        self.host: str = "https://ggst-game.guiltygear.com"

    def post(self, endpoint: str, message_pack) -> Union[list, None]:

        headers = {
            "User-Agent": "Steam",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        url: str = self.host + endpoint

        try:
            res = requests.post(url, data={"data": message_pack}, headers=headers)
        except ConnectionError as e:
            logging.exception(f"An error as occured: {e}")
            return None

        unpacked_res: list = msgpack.unpackb(res.content)

        return unpacked_res
