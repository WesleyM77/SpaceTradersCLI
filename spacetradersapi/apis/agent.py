from spacetradersapi import database
from spacetradersapi.apis import api


def create_agent(callsign, faction='COSMIC'):
    data = {
        'symbol': callsign,
        'faction': faction
    }
    response = api.post('register', data, False)
    data = response.json()['data']

    token = data['token']
    account_id = data['agent']['accountId']
    headquarters = data['agent']['headquarters']
    credit_amt = data['agent']['credits']

    database.insert_agent(callsign, faction, token, account_id, headquarters, credit_amt)

