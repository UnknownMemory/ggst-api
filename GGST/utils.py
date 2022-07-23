from .constants import PLAYSTATION, PC


def get_platform(platform: str) -> int:
    if platform.lower() == "playstation":
        return PLAYSTATION
    if platform.lower() == "pc":
        return PC
    raise ValueError("Platform not recognized. The platform should be either 'pc' or 'playstation'.")
