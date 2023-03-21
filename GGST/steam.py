"""
original code by Theoretical
https://github.com/Theoretical/ggst-py/blob/main/src/steam.py
"""

from binascii import crc32, hexlify
from typing import Union

from requests import get
from socket import inet_aton
from steam.core.msg import MsgProto
from steam.enums.emsg import EMsg
from steam.client import SteamClient
from steam.utils.proto import proto_fill_from_dict
from struct import pack
from time import time

game_tokens = []


def on_game_tokens(msg):
    global game_tokens
    game_tokens.extend(msg.body.tokens)


def create_auth_ticket(token, session_time):
    session_size = 24
    public_ip = get("https://checkip.amazonaws.com").text.strip()

    msg = b""
    msg += pack("I", len(token))
    msg += token
    msg += pack("III", session_size, 1, 2)

    ip = inet_aton(public_ip)
    ip = bytearray(ip)
    ip.reverse()

    msg += ip
    msg += pack("III", 0, int(session_time), 1)

    return msg


def steam_login(user: str, password: str) -> dict:
    global game_tokens

    app_id: int = 1384160  # Strive appId
    client: SteamClient = SteamClient()
    client.on(EMsg.ClientGameConnectTokens, on_game_tokens)
    session_time = time()
    client.cli_login(user, password)

    app_ticket = client.get_app_ticket(app_id).ticket
    auth_ticket = create_auth_ticket(game_tokens[0], time() - session_time)
    crc = crc32(auth_ticket)

    message = MsgProto(EMsg.ClientAuthList)
    message.body.tokens_left = len(game_tokens)
    message.body.app_ids.extend([app_id])

    tickets = message.body.tickets.add()

    ticket: dict[str, Union[int, bytes]] = {"gameid": app_id, "ticket": auth_ticket, "ticket_crc": crc}

    proto_fill_from_dict(tickets, ticket)

    resp = client.send_message_and_wait(message, EMsg.ClientAuthListAck)

    # build login token
    msg = auth_ticket
    msg += pack("I", len(app_ticket))
    msg += app_ticket

    return {"id": client.user.steam_id.as_64, "token": hexlify(msg).decode().upper()}
