"""Sensor platform for AREDN Mesh Weather."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, UnitOfSpeed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ArednMeshWeatherCoordinator
from .parser import ArednMeshWeatherData


@dataclass(frozen=True, kw_only=True)
class ArednMeshWeatherSensorEntityDescription(SensorEntityDescription):
    """Describes a AREDN Mesh Weather sensor entity."""

    value_fn: Callable[[ArednMeshWeatherData], int | float | str | None]
    attr_fn: Callable[[ArednMeshWeatherData], dict[str, Any]] | None = None


SENSOR_TYPES: tuple[ArednMeshWeatherSensorEntityDescription, ...] = (
    ArednMeshWeatherSensorEntityDescription(
        key="aqi",
        translation_key="aqi",
        device_class=SensorDeviceClass.AQI,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.aqi,
    ),
    ArednMeshWeatherSensorEntityDescription(
        key="pm25",
        translation_key="pm25",
        device_class=SensorDeviceClass.PM25,
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.pm25,
    ),
    ArednMeshWeatherSensorEntityDescription(
        key="alerts",
        translation_key="nws_alerts",
        icon="mdi:alert",
        value_fn=lambda data: len(data.alerts),
        attr_fn=lambda data: {"alerts": [alert["properties"] for alert in data.alerts]},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: ArednMeshWeatherCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        ArednMeshWeatherSensor(coordinator, entry, description)
        for description in SENSOR_TYPES
    )


class ArednMeshWeatherSensor(
    CoordinatorEntity[ArednMeshWeatherCoordinator], SensorEntity
):
    """AREDN Mesh Weather sensor entity."""

    entity_description: ArednMeshWeatherSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: ArednMeshWeatherCoordinator,
        entry: ConfigEntry,
        description: ArednMeshWeatherSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id}-{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
        )

    @property
    def native_value(self) -> int | float | str | None:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return the state attributes."""
        if self.entity_description.attr_fn:
            return self.entity_description.attr_fn(self.coordinator.data)
        return None
