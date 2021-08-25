"""
Create Events for the mac calendar.app
To schedule Just In capture
"""
# Built-in

# Special
import click

# App
from lib import collect_info
from lib import create_events
from lib.config import App

app = App()


def print_headers() -> None:
    """
    Print common headers for each app run.
    """
    click.echo("=" * 30)
    click.echo("| video capture scheduling app")
    click.echo("=" * 30)
    pass


def print_footer() -> None:
    """
    Print common footer for each app run.
    """
    click.echo("=" * 30)
    click.echo("| process complete!")
    click.echo("=" * 30)
    pass


@click.group()
def main() -> None:
    """
    Simple CLI to create mac calendar.app events to schedule Just In capture
    """
    pass


@main.command()
@click.argument("create-event")
def create_event(create_event: click.command) -> None:
    """
    Create the calendar events.

    arguments:
    create_event -- the name of the event to be created [ string ]

    example:
    app.py create-event 'cool event name'

    """
    print_headers()

    event_name = create_event.title().replace(" ", "_")

    answer = click.confirm(
        f"-> Do you want to create an event(s) named: '{event_name}' ?"
    )
    if not answer:
        click.echo("Great! Quitting the app.")
        print_footer()
        exit()

    click.echo(f"Okay, lets collect a little information.")
    click.echo(f"Answer each question folowed by <return>")

    info = collect_info.EventInfo(event_name)
    info.request_info()

    click.echo(f"Converting the info to calendar events...")

    events = create_events.CalendarEvents()
    events.build_events(info)

    print_footer()


if __name__ == "__main__":
    main()
