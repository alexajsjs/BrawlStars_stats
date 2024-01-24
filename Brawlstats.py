import json

import requests as req
from urllib import parse

# Authentication
auth = {
    "Authorization": ""
}


# Functions
def player_data(player: str):  # Getting player data
    url = f"https://api.brawlstars.com/v1/players/{parse.quote(player)}"

    response = req.get(url, headers=auth)

    try:
        return response.json()
    except json.JSONDecodeError:
        return None


def match_data(player: str):  # Getting a players recent matches
    url = f"https://api.brawlstars.com/v1/players/{parse.quote(player)}/battlelog"

    response = req.get(url=url, headers=auth)

    try:
        return response.json()
    except json.JSONDecodeError:
        return None
