import sys
import logging
from requests import post

from GGST.crypt import decrypt_response_data


class Request:
    def __init__(self) -> None:
        self.host: str = "https://ggst-game.guiltygear.com/api/"

    def post(self, endpoint: str, message_pack) -> list:

        headers = {
            "User-Agent": "GGST/Steam",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-store",
            'x-client-version': '1',
        }
        url: str = self.host + endpoint

        try:
            res = post(url, data={"data": message_pack}, headers=headers)
        except ConnectionError as error:
            logging.exception("An error as occured: %s", error)
            sys.exit(1)

        return decrypt_response_data(res.content.hex())
