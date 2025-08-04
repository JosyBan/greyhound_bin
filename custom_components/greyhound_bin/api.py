import asyncio
from datetime import datetime, timedelta
import html
import json
import logging
import re
import socket
from typing import Any, Dict, Optional

from aiohttp import ClientError, ClientResponse, ClientSession
import async_timeout
from bs4 import BeautifulSoup, Tag

from .const import CALENDAR_URL, LOGIN_URL

_LOGGER = logging.getLogger(__name__)


class GreyhoundAPIError(Exception):
    """Exception raised for errors in the Greyhound API."""


class GreyhoundAPICommunicationError(GreyhoundAPIError):
    """Communication error with the API."""


class GreyhoundApiClient:
    """Client to interact with the Greyhound bin collection API."""

    def __init__(self, accountnumber: str, pin: str, session: ClientSession) -> None:
        """Initialize the client."""
        self.accountnumber = accountnumber
        self.pin = pin
        self._session = session
        self.logged_in = False

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        return_json: bool = True,
    ) -> Any:
        """Generic API request wrapper."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                ) as response:
                    self._verify_response_or_raise(response)

                    if return_json:
                        return await response.json()
                    return await response.text()

        except asyncio.TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise GreyhoundAPICommunicationError(msg) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise GreyhoundAPICommunicationError(msg) from exception
        except Exception as exception:
            msg = f"Unexpected error - {exception}"
            raise GreyhoundAPIError(msg) from exception

    @staticmethod
    def _verify_response_or_raise(response: ClientResponse) -> None:
        """Verify HTTP response or raise error."""
        if response.status >= 400:
            raise GreyhoundAPIError(f"HTTP error: {response.status}")

    async def login(self) -> None:
        """Perform login to the Greyhound API."""
        try:
            text = await self._api_wrapper("GET", LOGIN_URL, return_json=False)
            soup = BeautifulSoup(text, "html.parser")
            token_input = soup.find("input", {"name": "csrfmiddlewaretoken"})

            if not token_input or not isinstance(token_input, Tag):
                raise GreyhoundAPIError("CSRF token input not found or not a Tag")

            csrf_token = token_input.get("value")

            if not csrf_token:
                raise GreyhoundAPIError("CSRF token missing 'value' attribute")

            csrf_token = token_input["value"]

            login_data = {
                "csrfmiddlewaretoken": csrf_token,
                "customerNo": self.accountnumber,
                "pinCode": self.pin,
            }

            headers = {
                "Referer": LOGIN_URL,
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            login_resp = await self._session.post(
                LOGIN_URL, data=login_data, headers=headers
            )

            login_text = await login_resp.text()

            if "Dashboard" not in login_text and "Logout" not in login_text:
                _LOGGER.error("Login failed. 'Logout' not found in response body.")
                raise GreyhoundAPIError(
                    "Login failed: Possibly invalid credentials or unexpected response."
                )

            _LOGGER.debug("Login successful for user %s", self.accountnumber)
            self.logged_in = True

        except ClientError as err:
            _LOGGER.exception("HTTP error during login: %s", err)
            raise GreyhoundAPIError("HTTP error during login.") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error during login: %s", err)
            raise

    async def async_get_data(self) -> dict[str, Any]:
        """Fetch bin collection events for the next 30 days."""
        if not self.logged_in:
            await self.login()

        calendar_text = await self._api_wrapper("GET", CALENDAR_URL, return_json=False)

        # Extract embedded JS data with regex
        match = re.search(r'var data = "(.*?)getJSONData', calendar_text, re.DOTALL)
        if not match:
            raise GreyhoundAPIError("Could not find embedded calendar data.")

        raw_data_str = match.group(1)
        unescaped = html.unescape(raw_data_str)

        json_match = re.search(r'({.*?})"', unescaped, re.DOTALL)
        if not json_match:
            raise GreyhoundAPIError("Failed to extract JSON payload.")

        try:
            raw_json = json.loads(json_match.group(1))
            collection_days = raw_json["data"]["collection_days"]
        except (json.JSONDecodeError, KeyError) as err:
            _LOGGER.exception("JSON parsing failed.")
            raise GreyhoundAPIError("Invalid calendar data format.") from err

        # Filter events within next 30 days
        today = datetime.now().date()
        cutoff = today + timedelta(days=30)
        events = []

        for date_str, bins in collection_days.items():
            try:
                event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                _LOGGER.warning("Skipping invalid date format: %s", date_str)
                continue

            if today <= event_date <= cutoff:
                waste_types = [
                    b["waste_types"][0] for b in bins if b.get("waste_types")
                ]
                events.append(
                    {
                        "date": event_date,
                        "bins": waste_types,
                    }
                )

        _LOGGER.info("Fetched %d bin collection events", len(events))

        # Build summary sensor data
        summary: dict[str, Any] = {}
        if events:
            next_event = events[0]  # assume sorted by date
            days_until = (next_event["date"] - today).days

            summary = {
                "next_collection_date": next_event["date"].isoformat(),
                "bin_types": ", ".join(next_event["bins"]),
                "days_until_collection": days_until,
                "collection_status": (
                    "Today"
                    if days_until == 0
                    else "Tomorrow" if days_until == 1 else f"In {days_until} days"
                ),
                # "service_disruption": next_event["cancelled"],
            }

        return {
            "events": events,  # calendar uses this
            "sensors": summary,  # sensors use this
        }
