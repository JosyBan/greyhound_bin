import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import ConfigEntryAuthFailed

from greyhound_bin.custom_components.greyhound_bin.data import GreyhoundConfigEntry

from .api import GreyhoundAPICommunicationError, GreyhoundApiClient, GreyhoundAPIError
from .const import DOMAIN, UPDATE_INTERVAL_DAYS

_LOGGER = logging.getLogger(__name__)


class GreyhoundDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch bin events from Greyhound."""

    config_entry: GreyhoundConfigEntry

    async def _async_update_data(self) -> Any:
        """Fetch data from API client."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except GreyhoundAPICommunicationError as err:
            raise ConfigEntryAuthFailed(err) from err
        except GreyhoundAPIError as err:
            raise UpdateFailed(err) from err
