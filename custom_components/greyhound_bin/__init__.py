"""Custom integration to integrate Greyhound Bin with Home Assistant."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import GreyhoundApiClient
from .const import CONF_ACCNO, CONF_PIN, DOMAIN, LOGGER, UPDATE_INTERVAL_DAYS
from .coordinator import GreyhoundDataUpdateCoordinator
from .data import GreyhoundData

if TYPE_CHECKING:
    from .data import GreyhoundConfigEntry

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.CALENDAR]


async def async_setup_entry(hass: HomeAssistant, entry: GreyhoundConfigEntry) -> bool:
    """Set up Greyhound Bin from a config entry."""

    coordinator = GreyhoundDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(days=UPDATE_INTERVAL_DAYS),
    )
    entry.runtime_data = GreyhoundData(
        client=GreyhoundApiClient(
            accountnumber=entry.data[CONF_ACCNO],
            pin=entry.data[CONF_PIN],
            session=async_get_clientsession(hass),
        ),
        coordinator=coordinator,
        integration=async_get_loaded_integration(hass, entry.domain),
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryAuthFailed as err:
        raise ConfigEntryAuthFailed(f"Auth failed during setup: {err}") from err

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: GreyhoundConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: GreyhoundConfigEntry) -> None:
    """Reload a config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
