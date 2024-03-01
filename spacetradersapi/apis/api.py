import requests
from spacetradersapi import database

base_url = 'https://api.spacetraders.io/v2/'


def post(url, data=None, use_token=True) -> requests.Response:
    headers = {}
    if use_token:
        bearer_token = database.get_bearer_token()
        headers['Authorization'] = 'Bearer ' + bearer_token

    return requests.post(base_url + url, data, headers=headers)

