"""Weather platform for AREDN Mesh Weather."""

from __future__ import annotations

from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_NATIVE_WIND_SPEED,
    ATTR_FORECAST_PRECIPITATION,
    ATTR_FORECAST_TIME,
    ATTR_FORECAST_WIND_BEARING,
    Forecast,
    WeatherEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, WMO_TO_HA_CONDITION
from .coordinator import ArednMeshWeatherCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the weather platform."""
    coordinator: ArednMeshWeatherCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ArednMeshWeatherEntity(coordinator, entry)])


class ArednMeshWeatherEntity(
    CoordinatorEntity[ArednMeshWeatherCoordinator], WeatherEntity
):
    """AREDN Mesh Weather entity."""

    _attr_has_entity_name = True
    _attr_name = None  # Use device name

    def __init__(
        self, coordinator: ArednMeshWeatherCoordinator, entry: ConfigEntry
    ) -> None:
        """Initialize the weather entity."""
        super().__init__(coordinator)
        self._attr_unique_id = entry.unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="AREDN",
            model="Mesh Weather Node",
        )

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        code = self.coordinator.data.condition_code
        return WMO_TO_HA_CONDITION.get(code)

    @property
    def native_temperature(self) -> float | None:
        """Return the temperature."""
        return self.coordinator.data.temperature

    @property
    def native_temperature_unit(self) -> str | None:
        """Return the unit of measurement for temperature."""
        if self.coordinator.data.temperature_unit == "°F":
            return UnitOfTemperature.FAHRENHEIT
        return UnitOfTemperature.CELSIUS

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure."""
        return self.coordinator.data.pressure

    @property
    def native_pressure_unit(self) -> str:
        """Return the unit of measurement for pressure."""
        return UnitOfPressure.HPA

    @property
    def humidity(self) -> float | None:
        """Return the humidity."""
        return self.coordinator.data.humidity

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed."""
        return self.coordinator.data.wind_speed

    @property
    def native_wind_speed_unit(self) -> str:
        """Return the unit of measurement for wind speed."""
        return UnitOfSpeed.MILES_PER_HOUR

    @property
    def wind_bearing(self) -> float | str | None:
        """Return the wind bearing."""
        return self.coordinator.data.wind_bearing

    @property
    def forecast(self) -> list[Forecast] | None:
        """Return the forecast."""
        return [
            {
                ATTR_FORECAST_TIME: f_item["datetime"],
                ATTR_FORECAST_CONDITION: WMO_TO_HA_CONDITION.get(f_item["condition"]),
                ATTR_FORECAST_NATIVE_TEMP: f_item["temperature"],
                ATTR_FORECAST_NATIVE_TEMP_LOW: f_item["templow"],
                ATTR_FORECAST_PRECIPITATION: f_item["precipitation"],
                ATTR_FORECAST_NATIVE_WIND_SPEED: f_item["wind_speed"],
                ATTR_FORECAST_WIND_BEARING: f_item["wind_bearing"],
            }
            for f_item in self.coordinator.data.forecast
        ]
