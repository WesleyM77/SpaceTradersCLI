import openapi_client
from openapi_client import ShipRequirements

from spacetradersapi import database, util
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime
from rich.panel import Panel
from rich.tree import Tree

console = Console()

configuration = openapi_client.Configuration(
    access_token=database.get_bearer_token()
)


def get_ships():
    with openapi_client.ApiClient(configuration) as api_client:
        api = openapi_client.FleetApi(api_client)
        page = 1
        limit = 10

        try:
            # List Ships
            api_response = api.get_my_ships(page=page, limit=limit)
            table = Table("Ship", "Type", "System", "Waypoint", "Status", "Flight Mode", "Source", "Destination",
                          "Arriving in",
                          "Cargo", "Fuel")
            for ship in api_response.data:
                eta = '-'
                if ship.nav.status == 'IN_TRANSIT':
                    arrival_in = ship.nav.route.arrival.replace(tzinfo=None)
                    today = datetime.utcnow()
                    eta = arrival_in - today
                    eta = str(eta)[0:-7]

                cargo = util.shade_percentage(ship.cargo.units, ship.cargo.capacity, full_good=False)
                fuel = util.shade_percentage(ship.fuel.current, ship.fuel.capacity)

                table.add_row(ship.symbol, ship.registration.role, ship.nav.system_symbol, ship.nav.waypoint_symbol,
                              ship.nav.status, ship.nav.flight_mode, ship.nav.route.origin.symbol,
                              ship.nav.route.destination.symbol, eta, cargo, fuel)
            console.print(table)
        except Exception as e:
            print("Exception when calling FleetApi->get_my_ships: %s\n" % e)


def get_ship(symbol: str):
    with openapi_client.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api = openapi_client.FleetApi(api_client)

        try:
            # Get Ship
            api_response = api.get_my_ship(symbol)
            print(api_response)
            tree = Tree(symbol)

            ship = api_response.data

            # Create the status table
            table = Table("Type", "System", "Waypoint", "Status", "Flight Mode", "Source", "Destination",
                          "Arriving in",
                          "Cargo", "Fuel")
            eta = '-'
            if ship.nav.status == 'IN_TRANSIT':
                arrival_in = ship.nav.route.arrival.replace(tzinfo=None)
                today = datetime.utcnow()
                eta = arrival_in - today
                eta = str(eta)[0:-7]

            cargo = str(ship.cargo.units) + '/' + str(ship.cargo.capacity)
            fuel = str(ship.fuel.current) + '/' + str(ship.fuel.capacity)

            table.add_row(ship.registration.role, ship.nav.system_symbol, ship.nav.waypoint_symbol,
                          ship.nav.status, ship.nav.flight_mode, ship.nav.route.origin.symbol,
                          ship.nav.route.destination.symbol, eta, cargo, fuel)

            panel = Panel.fit(
                table,
                title="Status",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create the crew table
            table = Table("Count", "Required", "Max", "Rotation", "Morale", "Wages")
            crew = ship.crew
            table.add_row(str(crew.current), str(crew.required), str(crew.capacity), crew.rotation, str(crew.morale),
                          str(crew.wages))
            panel = Panel.fit(
                table,
                title="Crew",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create frame table
            table = Table("Frame", "Name", "Condition", "Slots", "Mount Points", "Fuel Cap", "Requirements")
            frame = ship.frame
            table.add_row(frame.symbol, frame.name, str(frame.condition), str(frame.module_slots),
                          str(frame.mounting_points), str(frame.fuel_capacity), make_requirements(frame.requirements))
            panel = Panel.fit(
                table,
                title="Frame",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create reactor table
            table = Table("Reactor", "Name", "Condition", "Power Output", "Requirements")
            reactor = ship.reactor
            table.add_row(reactor.symbol, reactor.name, str(reactor.condition), str(reactor.power_output),
                          make_requirements(reactor.requirements))
            panel = Panel.fit(
                table,
                title="Reactor",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create engine table
            table = Table("Engine", "Name", "Condition", "Speed", "Requirements")
            engine = ship.engine
            table.add_row(engine.symbol, engine.name, str(engine.condition), str(engine.speed),
                          make_requirements(engine.requirements))
            panel = Panel.fit(
                table,
                title="Engine",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create module table
            table = Table("Module", "Name", "Capacity", "Range", "Requirements")
            for module in ship.modules:
                table.add_row(module.symbol, module.name, str(module.capacity), module.range,
                              make_requirements(module.requirements))
            panel = Panel.fit(
                table,
                title="Modules",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create mounts table
            table = Table("Mount", "Name", "Strength",  "Requirements")
            for mount in ship.mounts:
                table.add_row(mount.symbol, mount.name, str(mount.strength),
                              make_requirements(mount.requirements))
            panel = Panel.fit(
                table,
                title="Mounts",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            # Create cargo table
            table = Table("Name", "Units")
            for item in ship.cargo.inventory:
                table.add_row(item.name, item.units)
            if table.row_count == 0:
                table = 'Empty Cargo Hold'
            panel = Panel.fit(
                table,
                title="Cargo",
                border_style="red",
                title_align="left",
                padding=(1, 2),
            )
            tree.add(panel)

            console.print(tree)
        except Exception as e:
            print("Exception when calling FleetApi->get_my_ship: %s\n" % e)


def make_requirements(req: ShipRequirements) -> str:
    ret = ''
    if isinstance(req.power, int) and req.power > 0:
        ret = ret + str(req.power) + ' power'
    if isinstance(req.crew, int) and req.crew > 0:
        if ret != '':
            ret = ret + '; '
        ret = ret + str(req.crew) + ' crew'
    if isinstance(req.slots, int) and req.slots > 0:
        if ret != '':
            ret = ret + '; '
        ret = ret + str(req.slots) + ' slots'

    return ret
