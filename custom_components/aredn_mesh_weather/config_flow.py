"""Config flow for AREDN Mesh Weather integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DEFAULT_URL, DOMAIN
from .parser import InvalidData

_LOGGER = logging.getLogger(__name__)


class ArednMeshWeatherConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AREDN Mesh Weather."""

    VERSION = 1
    data_schema = vol.Schema({vol.Required(CONF_URL, default=DEFAULT_URL): str})

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Handle the initial step."""
        errors: dict[str, Any] = {}
        if user_input is not None:
            url = user_input[CONF_URL]
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                if data.get("status") != "ok" or "weather" not in data:
                    raise InvalidData

                await self.async_set_unique_id(url)
                self._abort_if_unique_id_configured(updates={CONF_URL: url})

                return self.async_create_entry(
                    title=data["geo"]["node"], data=user_input
                )
            except (aiohttp.ClientError, TimeoutError) as err:
                _LOGGER.warning("Failed to connect to '%s': %s", url, err)
                return self.async_show_form(
                    step_id="user",
                    data_schema=self.data_schema,
                    errors={"base": "cannot_connect"},
                    description_placeholders={"error_details": str(err)},
                )
            except InvalidData:
                return self.async_show_form(
                    step_id="user",
                    data_schema=self.data_schema,
                    errors={"base": "invalid_data"},
                )
            except Exception:  # pylint: disable=broad-except-clause
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=self.data_schema,
            errors=errors,
        )
