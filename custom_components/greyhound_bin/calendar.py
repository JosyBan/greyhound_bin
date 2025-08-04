from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from homeassistant.components.calendar import CalendarEntity, CalendarEvent

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import GreyhoundDataUpdateCoordinator
    from .data import GreyhoundConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: GreyhoundConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities([GreyhoundBinCalendar(coordinator)])


class GreyhoundBinCalendar(CalendarEntity):
    """Calendar entity for Greyhound bin collections."""

    def __init__(self, coordinator: GreyhoundDataUpdateCoordinator) -> None:
        self.coordinator = coordinator
        self._attr_name = "Greyhound Bin Collection"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_calendar"

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        now = datetime.now().date()
        events = self.coordinator.data.get("events", [])

        for event in events:
            event_date = event.get("date")
            if isinstance(event_date, datetime):
                event_date = event_date.date()

            if event_date >= now:
                bins = event.get("bins", [])
                # Format bins with colored squares
                bin_labels = []
                if "GREEN" in bins:
                    bin_labels.append("🟩 Green Bin")
                else:
                    bin_labels.append("🟫⬛ Brown & Black Bins")
                # Add any other bin types here as needed

                summary = (
                    f"Bin Collection: {', '.join(bin_labels)}"
                    if bin_labels
                    else "Bin Collection"
                )
                return CalendarEvent(
                    summary=summary,
                    start=event_date,
                    end=event_date + timedelta(days=1),
                )

        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events between start and end."""
        events = self.coordinator.data.get("events", [])
        result = []

        for event in events:
            date = event["date"]
            if isinstance(date, datetime):
                date = date.date()

            if start_date.date() <= date < end_date.date():
                bins = event.get("bins", [])
                bin_labels = []
                if "GREEN" in bins:
                    bin_labels.append("🟩 Green Bin")
                else:
                    bin_labels.append("🟫⬛ Brown & Black Bins")

                summary = (
                    f"Bin Collection: {', '.join(bin_labels)}"
                    if bin_labels
                    else "Bin Collection"
                )

                result.append(
                    CalendarEvent(
                        summary=summary,
                        start=date,
                        end=date + timedelta(days=1),
                    )
                )
        return result
