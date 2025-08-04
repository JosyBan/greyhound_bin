"""Adds config flow for greyhound_bin."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import voluptuous as vol

from .api import GreyhoundApiClient, GreyhoundAPIError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Form schema for step_user
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("account number"): str,
        vol.Required("pin"): str,
    }
)


class GreyhoundBinConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Greyhound Bin integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL
    _reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input["account number"])
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            client = GreyhoundApiClient(
                user_input["account number"], user_input["pin"], session
            )

            try:
                await client.login()

                return self.async_create_entry(
                    title=f"Greyhound Bin ({user_input['account number']})",
                    data=user_input,
                )

            except GreyhoundAPIError:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected error during config flow")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "account number",
                        default=(user_input or {}).get("account number", ""),
                    ): str,
                    vol.Required("pin", default=(user_input or {}).get("pin", "")): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> ConfigFlowResult:
        """Handle re-authentication with updated credentials."""
        entry_id = self.context.get("entry_id")

        if not entry_id:
            _LOGGER.warning("No entry_id in reauth context.")
            return self.async_abort(reason="missing_entry_id")

        self._reauth_entry = self.hass.config_entries.async_get_entry(entry_id)

        return await self.async_step_user()

    async def async_step_import(self, user_input: dict[str, Any]) -> ConfigFlowResult:
        """Handle import from YAML config."""
        return await self.async_step_user(user_input)
