"""
Create Calendar Events
"""
# Built-in
from datetime import datetime, timedelta
import pathlib
from subprocess import call
import uuid
from zoneinfo import ZoneInfo

# Special
import click
from icalendar import Calendar, Event, vText

# App
from .collect_info import EventInfo
from lib.config import App

app = App()


class CalendarEvents:
    def __init__(self) -> None:
        pass

    def build_events(self, info: EventInfo) -> None:
        """
        Create calendar(s) and event(s) based on the event info. Then dump each calendar to an .ics file.
        """

        # Each capture feed is a separate calendar
        for feed in info.feed_names:

            # Create the calendar
            cal = Calendar()
            # Generate required calendar properties
            cal.add("prodid", f"-//{app.app_name}//Just:In Schedule//EN")
            cal.add("version", "2.0")

            repeat_week_no = 0
            while repeat_week_no < int(info.repeat_weeks):

                the_date = info.event_date.replace(
                    tzinfo=ZoneInfo(app.default_timezone)
                )
                the_date = the_date + timedelta(days=(7 * repeat_week_no))

                i = 0
                while i < len(info.event_times) - 1:

                    item_no = "{0:0>2}".format(i + 1)
                    the_month_s = "{0:0>2}".format(the_date.month)
                    the_day_s = "{0:0>2}".format(the_date.day)

                    event = Event()
                    if info.time_string is not None:
                        event.add(
                            "summary",
                            "{}-{}_{}_{}-{}-{}-{}".format(
                                info.event_title,
                                the_date.year,
                                the_month_s,
                                the_day_s,
                                info.time_string,
                                feed,
                                item_no,
                            ),
                        )
                    else:
                        event.add(
                            "summary",
                            "{}-{}_{}_{}-{}-{}".format(
                                info.event_title,
                                the_date.year,
                                the_month_s,
                                the_day_s,
                                feed,
                                item_no,
                            ),
                        )

                    # Combine date and time
                    datetime_i = datetime.combine(the_date.date(), info.event_times[i])
                    event.add(
                        "dtstart",
                        datetime_i,
                    )
                    datetime_i_1 = datetime.combine(
                        the_date.date(), info.event_times[i + 1]
                    )
                    event.add(
                        "dtend",
                        datetime_i_1,
                    )

                    event.add(
                        "dtstamp", datetime.now(tz=ZoneInfo(app.default_timezone))
                    )
                    event["description"] = vText(info.event_description)
                    event["location"] = vText(info.event_location)

                    # Source for this:http://www.kanzaki.com/docs/ical/uid.html
                    event["uid"] = (
                        datetime.now().strftime("%Y%m%dT%H%M%S")
                        + "/"
                        + str(uuid.uuid1())
                        + "@"
                        + app.hostname
                    )

                    # Add the event to the calendar
                    cal.add_component(event)
                    i += 1

                repeat_week_no += 1

            self.write_ics_file(info, feed, cal)

        # Open the exported .ics files in the Finder
        click.echo("Opening Finder folder...")
        call(["open", info.export_path_input])

    def write_ics_file(self, info: EventInfo, feed: str, cal: Calendar) -> None:
        """
        Write the ics file with the correct file naming.
        """

        if info.time_string is not None:
            file_string = "{}-{}-{}-Events".format(
                info.event_title, info.time_string, feed
            )

        else:
            file_string = "{}-{}-Events".format(info.event_title, feed)

        try:
            file = pathlib.Path.joinpath(
                pathlib.Path(info.export_path_input), f"{file_string}.ics"
            )
            click.echo(f"Writing to:{file}...")

            with open(file, "wb") as f:
                f.write(cal.to_ical())

        except Exception as exp:
            click.echo(f"Exception:{exp}")
            click.echo("Exiting...")
            exit()
