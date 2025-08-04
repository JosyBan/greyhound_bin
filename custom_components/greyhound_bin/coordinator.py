import logging
from typing import Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import GreyhoundAPICommunicationError, GreyhoundAPIError
from .data import GreyhoundConfigEntry

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
