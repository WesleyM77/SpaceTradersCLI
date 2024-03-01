import openapi_client
from spacetradersapi import database
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.console import Console

console = Console()

configuration = openapi_client.Configuration(
    access_token=database.get_bearer_token()
)


def get_waypoint_info(system, waypoint):
    with openapi_client.ApiClient(configuration) as api_client:
        api = openapi_client.SystemsApi(api_client)
        try:
            # Get Waypoint
            r = api.get_waypoint(system, waypoint)
            d = r.data

            columns = []

            table1 = Table("System", "Waypoint", "Type", "Coordinates")
            table1.add_row(d.system_symbol, d.symbol, d.type, str(d.x) + ", " + str(d.y))
            columns.append(table1)

            table2 = Table("Orbital")
            for orbital in d.orbitals:
                table2.add_row(orbital.symbol)
            columns.append(table2)

            table3 = Table("Trait", "Name")
            for trait in d.traits:
                table3.add_row(trait.symbol, trait.name)
            columns.append(table3)

            under_construction = 'Yes' if d.is_under_construction else 'No'
            construction = Panel(under_construction, title="Under Construction?")
            columns.append(construction)

            panel = Panel.fit(
                Columns(columns),
                title="Waypoint Data",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )

            console.print(panel)
        except Exception as e:
            print("Exception when calling SystemsApi->get_waypoint: %s\n" % e)
