"""Custom types for greyhound_bin integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import GreyhoundApiClient
    from .coordinator import GreyhoundDataUpdateCoordinator

# Typed ConfigEntry with attached runtime data
type GreyhoundConfigEntry = ConfigEntry[GreyhoundData]


@dataclass
class GreyhoundData:
    """Runtime data stored in config entry for greyhound_bin."""

    client: GreyhoundApiClient
    coordinator: GreyhoundDataUpdateCoordinator
    integration: Integration
