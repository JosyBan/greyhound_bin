from __future__ import annotations
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, List



if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.components.calendar import CalendarEntity, CalendarEvent 

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
            if not isinstance(event_date, datetime):
                event_date = datetime.combine(event_date, datetime.min.time())
            if event_date.date() >= now:
                summary = f"Bin Collection: {', '.join(event.get('bins', []))}"
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
        return [
            CalendarEvent(
                summary=f"Bin Collection: {', '.join(event.get('bins', []))}",
                start=datetime.combine(event["date"], datetime.min.time()),
                end=datetime.combine(event["date"], datetime.min.time()) + timedelta(days=1),
            )
            for event in events
            if start_date.date() <= event["date"] <= end_date.date()
        ]
