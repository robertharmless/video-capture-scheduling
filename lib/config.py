"""
Configuration Settings.
"""
# Built-in
from os import environ
import socket


class App:
    """
    App configs
    """

    hostname = None
    app_name = "video-capture-scheduling"
    default_timezone = None

    def __init__(self) -> None:

        self.hostname = socket.gethostname()
        # Set these in environmental variables.
        # Timezone options can be found at:
        # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        # Or:
        # zoneinfo.available_timezones()

        self.default_timezone = environ["TIMEZONE"]
