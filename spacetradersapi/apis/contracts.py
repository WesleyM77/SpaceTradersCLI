from datetime import datetime
import openapi_client
from spacetradersapi import database, util
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

configuration = openapi_client.Configuration(
    access_token=database.get_bearer_token()
)


def get_contracts():
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api = openapi_client.ContractsApi(api_client)
        page = 1  # int | What entry offset to request (optional) (default to 1)
        limit = 10  # int | How many entries to return per page (optional) (default to 10)

        try:
            # List Contracts
            r = api.get_contracts(page=page, limit=limit)

            table = Table("ID", "Faction", "Deadline In", "Accept In", "Reward", "Accepted",
                          "Deliver")
            for c in r.data:
                if c.fulfilled:
                    continue
                fulfilled = c.fulfilled
                until_deadline = '-'
                if not fulfilled:
                    deadline = c.terms.deadline.replace(tzinfo=None)
                    today = datetime.utcnow()
                    until_deadline = deadline - today
                    until_deadline = str(until_deadline)[0:-10]

                accepted = c.accepted
                accepted_string = util.yes_no(accepted)
                until_accept_deadline = '-'
                if not accepted:
                    accept_deadline = c.deadline_to_accept.replace(tzinfo=None)
                    today = datetime.utcnow()
                    until_accept_deadline = accept_deadline - today
                    until_accept_deadline = str(until_accept_deadline)[0:-10]

                deliveries = ''
                for good in c.terms.deliver:
                    if deliveries != '':
                        deliveries += '\n'
                    deliveries += str(good.units_required - good.units_fulfilled) + ' ' + good.trade_symbol + ' to ' + good.destination_symbol

                rewards = str(c.terms.payment.on_accepted) + '/' + str(c.terms.payment.on_fulfilled)

                table.add_row(c.id, c.faction_symbol, until_deadline, until_accept_deadline, rewards,
                              accepted_string, deliveries)

            print(table)
        except Exception as e:
            print("Exception when calling ContractsApi->get_contracts: %s\n" % e)