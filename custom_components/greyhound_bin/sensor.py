"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription,SensorDeviceClass

from .entity import GreyhoundBinEntity  

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import GreyhoundDataUpdateCoordinator
    from .data import GreyhoundConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="next_collection_date",
        name="Next Collection Date",
        icon="mdi:calendar",
        device_class=SensorDeviceClass.DATE,
    ),
    SensorEntityDescription(
        key="bin_types",
        name="Bin Types Being Collected",
        icon="mdi:delete-empty",
    ),
    SensorEntityDescription(
        key="days_until_collection",
        name="Days Until Next Collection",
        icon="mdi:timer-sand",
        device_class=SensorDeviceClass.DURATION,
    ),
    SensorEntityDescription(
        key="collection_status",
        name="Collection Status",
        icon="mdi:calendar-check",
    ),
    SensorEntityDescription(
        key="service_disruption",
        name="Service Disruption Alert",
        icon="mdi:alert-circle",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: GreyhoundConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        GreyhoundBinSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class GreyhoundBinSensor(GreyhoundBinEntity, SensorEntity):
    """Representation of a Greyhound bin collection sensor."""

    def __init__(
        self,
        coordinator: GreyhoundDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_should_poll = False

    @property
    def native_value(self) -> str | None: # type: ignore
        """Return the native value of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("sensors", {}).get(self.entity_description.key)

    
    @property
    def available(self) -> bool: # type: ignore
        """Return True if entity data is available."""
        return self.coordinator.last_update_success