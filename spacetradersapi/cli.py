from typing import Optional
import typer
from spacetradersapi import __app_name__, __version__, database
from spacetradersapi.apis import agent, systems, fleets, default, contracts

app = typer.Typer()
# cd .\PycharmProjects\SpaceTradersCLI\
# venv/Scripts/activate.ps1


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


# ============================================================= CLI/App Commands
@app.command()
def init() -> None:
    """
    Initializes the database; WIPES EVERYTHING;
    """
    database.init_db()


# ============================================================= Agent Commands
# TODO: Upgrade to new API
@app.command()
def create_agent(callsign: str, faction: str = 'COSMIC'):
    """
    Creates a new agent with CALLSIGN and optional FACTION
    """
    agent.create_agent(callsign, faction)


# ============================================================= System Commands
@app.command()
def get_waypoint_info(system: str, waypoint: str):
    """
    Outputs data about the WAYPOINT in SYSTEM
    """
    systems.get_waypoint_info(system, waypoint)


# ============================================================= Fleet Commands
@app.command()
def get_ships():
    """
    Outputs data about your ships
    """
    fleets.get_ships()


@app.command()
def get_ship(ship: str):
    """
    Outputs data about your SHIP
    """
    fleets.get_ship(ship)


# ============================================================= Default Commands
@app.command()
def status():
    """
    Outputs SpaceTraders API status
    """
    default.status()


# ============================================================= Contract Commands
@app.command()
def get_contracts():
    """
    Gets available contracts
    """
    contracts.get_contracts()