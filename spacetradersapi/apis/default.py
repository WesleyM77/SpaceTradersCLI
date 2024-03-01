from datetime import datetime
import openapi_client
from spacetradersapi import database
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()
configuration = openapi_client.Configuration(
    access_token=database.get_bearer_token()
)


def status():
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = openapi_client.DefaultApi(api_client)

        try:
            # Get Status
            r = api_instance.get_status()
            s = r.stats

            # Calculate time until reset
            reset_on = datetime.strptime(r.server_resets.next, '%Y-%m-%dT%H:00:00.000Z')
            today = datetime.utcnow()
            until = reset_on - today
            until = str(until)[0:-10]

            table = Table("Status", "Version", "Reset Date", "Next Reset In", "Agents", "Ships", "Systems", "Waypoints")
            table.add_row(r.status, r.version, r.reset_date, until, str(s.agents), str(s.ships), str(s.systems), str(s.waypoints))
            console.print(table)

            table = Table("Link", "URL")
            for link in r.links:
                table.add_row(link.name, link.url)
            console.print(table)

        except Exception as e:
            print("Exception when calling DefaultApi->get_status: %s\n" % e)

