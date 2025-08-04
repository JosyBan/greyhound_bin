"""Constants for greyhound_bin."""

from logging import Logger, getLogger

# Base component constants
DOMAIN = "greyhound_bin"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/JosyBan/greyhound_bin/issues"


# Configuration and options
CONF_ACCNO = "account number"
CONF_PIN = "pin"

# Logging
LOGGER: Logger = getLogger(__package__)


# API URLs
LOGIN_URL = "https://app.greyhound.ie/"
CALENDAR_URL = "https://app.greyhound.ie/collection/collection_calendar"


UPDATE_INTERVAL_DAYS = 1