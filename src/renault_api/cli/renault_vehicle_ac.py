"""CLI function for a vehicle."""
from typing import Any
from typing import Dict

import aiohttp
import click
import dateparser
from tabulate import tabulate

from . import renault_vehicle


async def start(
    websession: aiohttp.ClientSession,
    ctx_data: Dict[str, Any],
    temperature: int,
    at: str,
) -> None:
    """Start air conditionning."""
    vehicle = await renault_vehicle.get_vehicle(
        websession=websession, ctx_data=ctx_data
    )
    if at:
        when = dateparser.parse(at)
    else:
        when = None
    response = await vehicle.set_ac_start(temperature=temperature, when=when)
    click.echo(response.raw_data)


async def cancel(
    websession: aiohttp.ClientSession,
    ctx_data: Dict[str, Any],
) -> None:
    """Cancel air conditionning."""
    vehicle = await renault_vehicle.get_vehicle(
        websession=websession, ctx_data=ctx_data
    )
    response = await vehicle.set_ac_stop()
    click.echo(response.raw_data)


async def history(
    websession: aiohttp.ClientSession,
    ctx_data: Dict[str, Any],
    start: str,
    end: str,
    period: str,
) -> None:
    """Display vehicle status."""
    vehicle = await renault_vehicle.get_vehicle(
        websession=websession, ctx_data=ctx_data
    )
    response = await vehicle.get_hvac_history(
        start=dateparser.parse(start), end=dateparser.parse(end), period=period
    )
    click.echo(response.raw_data)


async def sessions(
    websession: aiohttp.ClientSession,
    ctx_data: Dict[str, Any],
    start: str,
    end: str,
) -> None:
    """Display vehicle status."""
    vehicle = await renault_vehicle.get_vehicle(
        websession=websession, ctx_data=ctx_data
    )
    response = await vehicle.get_hvac_sessions(
        start=dateparser.parse(start), end=dateparser.parse(end)
    )
    click.echo(response.raw_data)

async def schedule(
    websession: aiohttp.ClientSession,
    ctx_data: Dict[str, Any],
) -> None:
    """Show or edit AC schedules."""
    vehicle = await renault_vehicle.get_vehicle(
        websession=websession, ctx_data=ctx_data
    )
    response = await vehicle.get_hvac_settings()
    click.echo(f"Schedule mode is: {response.mode}")
    headers = ["Nr.", "Active", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    table_data = []
    for schedule in response.schedules:
        row = [schedule.id, schedule.activated]
        for day in [schedule.monday, schedule.tuesday, schedule.wednesday, schedule.thursday, schedule.friday, schedule.saturday, schedule.sunday]:
            if day is not None:
                row.append(day.readyAtTime)
            else:
                row.append("---")
        table_data.append(row)

    click.echo(tabulate(table_data, headers=headers))
