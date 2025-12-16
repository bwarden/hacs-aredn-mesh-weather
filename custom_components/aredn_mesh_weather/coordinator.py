"""DataUpdateCoordinator for the AREDN Mesh Weather integration."""

from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .parser import ArednMeshWeatherData, InvalidData

_LOGGER = logging.getLogger(__name__)


class ArednMeshWeatherCoordinator(DataUpdateCoordinator[ArednMeshWeatherData]):
    """AREDN Mesh Weather coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.url = entry.data[CONF_URL]
        self.session = async_get_clientsession(hass)

        # Set a short initial update interval. This will be adjusted after the first successful fetch.
        super().__init__(
            hass,
            _LOGGER,
            name="AREDN Mesh Weather",
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self) -> ArednMeshWeatherData:
        """Fetch data from the AREDN Mesh Weather device."""
        try:
            async with self.session.get(self.url, timeout=10) as response:
                if response.status != 200:
                    raise UpdateFailed(f"Error fetching data: HTTP {response.status}")

                data = await response.json()
                parsed_data = ArednMeshWeatherData.from_dict(data)

                # The API provides a recommended update interval.
                # We'll use that, but ensure it's at least 60 seconds.
                new_interval = max(parsed_data.update_interval, timedelta(seconds=60))
                if (
                    self.update_interval != new_interval
                    and new_interval.total_seconds() > 0
                ):
                    self.update_interval = new_interval
                    _LOGGER.info("Adjusting update interval to %s", new_interval)

                return parsed_data

        except (aiohttp.ClientError, TimeoutError) as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except (ValueError, KeyError, InvalidData) as err:
            raise UpdateFailed(f"Invalid data received from API: {err}") from err
