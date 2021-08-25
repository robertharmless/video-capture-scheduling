"""
Collect Event Information
"""
# Built-in
import datetime

# Special
import click

# App
from lib.config import App

app = App()


class EventInfo:
    event_title = None
    event_date = None
    repeat_weeks = None
    time_string = None
    feed_names = []
    event_location = None
    event_description = None
    event_times = []
    export_path_input = None

    def __init__(self, event_title) -> None:
        self.event_title = event_title

    def request_info(self) -> None:
        """
        Collect information from user.
        """

        # Number of questions to ask
        q_total = 8
        # Current question number
        q_count = 0

        q_count += 1
        self.event_date = click.prompt(
            f"[ {q_count} of {q_total} ] Please enter the event date",
            type=click.DateTime(formats=["%Y-%m-%d"]),
        )
        self.event_month_string = "{0:0>2}".format(self.event_date.month)
        self.event_day_string = "{0:0>2}".format(self.event_date.day)

        click.echo(
            "-> Build a list of record times - minimum of 2 entries - as military time [ 17:30 ]"
        )
        q_count += 1
        time_count = 0
        event_times_list = []
        empty_time = datetime.time(0, 0, 0)

        while True:
            time_count += 1
            the_time = click.prompt(
                f"[ {q_count} of {q_total} ] Enter Time {time_count} formatted as [ HH:MM ]",
                type=click.DateTime(formats=["%H:%M"]),
                default="0:0",
                show_default=False,
            )

            if the_time.time() == empty_time:
                break

            self.event_times.append(the_time.time())

            event_times_list.append(str(the_time.time()))
            event_times_string = " - ".join(event_times_list)
            click.echo(f"Times -> {event_times_string}")

        q_count += 1
        self.repeat_weeks = click.prompt(
            f"[ {q_count} of {q_total} ] Enter the number of weeks to repeat [ enter 1 if it occurs once ]",
            type=int,
            default=1,
            show_default=False,
        )

        q_count += 1
        time_string_input = click.prompt(
            f"[ {q_count} of {q_total} ] Enter a time string to add to the event name [ format as 0130PM ]",
            type=str,
            default="",
            show_default=False,
        )
        if time_string_input != "":
            self.time_string = "{0:0>6}".format(time_string_input.upper())

        q_count += 1
        event_location_input = click.prompt(
            f"[ {q_count} of {q_total} ] Please enter the Location of the event",
            type=str,
            default="",
            show_default=False,
        )
        self.event_location = event_location_input.title()

        q_count += 1
        event_description_input = click.prompt(
            f"[ {q_count} of {q_total} ] Please enter a Description of the event",
            type=str,
            default="",
            show_default=False,
        )
        self.event_description = event_description_input.capitalize()

        click.echo("-> Build a list of feeds to capture.")
        q_count += 1
        feed_count = 0
        while 1:
            feed_count += 1
            feed_name = click.prompt(
                f"[ {q_count} of {q_total} ] Enter the name a Feed {feed_count}",
                type=str,
                default="",
                show_default=False,
            )

            if feed_name == "":
                break

            self.feed_names.append(feed_name.upper())
            feed_string = " - ".join(self.feed_names)
            click.echo(f"Feeds -> {feed_string}")

        q_count += 1
        self.export_path_input = click.prompt(
            f"[ {q_count} of {q_total} ] Enter a folder path for the '.ics' files to be put in",
            type=click.Path(resolve_path=True, dir_okay=True, exists=True),
        )
