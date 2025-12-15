"""Parser for AREDN Mesh Weather data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


@dataclass
class ArednMeshWeatherData:
    """Data class for AREDN Mesh Weather."""

    # Static info
    node: str
    latitude: float
    longitude: float
    elevation: int
    update_time: datetime
    update_interval: timedelta

    # Current weather
    temperature: float
    temperature_unit: str
    humidity: int
    pressure: float
    wind_speed: float
    wind_bearing: int
    condition_code: int

    # Forecast
    forecast: list[dict[str, Any]]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ArednMeshWeatherData:
        """Create a new ArednMeshWeatherData object from a dictionary."""
        geo = data["geo"]
        weather = data["weather"]
        current = weather["current"]
        current_units = weather["current_units"]
        daily = weather["daily"]

        # Calculate next update time
        update_time_str = current["time"]
        interval_seconds = current["interval"]
        update_time = datetime.fromisoformat(update_time_str).astimezone(timezone.utc)

        # Create daily forecast
        forecast_data = []
        for i, time_str in enumerate(daily["time"]):
            forecast_item = {
                "datetime": time_str,
                "condition": daily["weathercode"][i],
                "temperature": daily["temperature_2m_max"][i],
                "templow": daily["temperature_2m_min"][i],
                "precipitation": daily["precipitation_sum"][i],
                "wind_speed": daily["wind_speed_10m_max"][i],
                "wind_bearing": daily["wind_direction_10m_dominant"][i],
            }
            forecast_data.append(forecast_item)

        return cls(
            node=geo["node"],
            latitude=geo["lat"],
            longitude=geo["lon"],
            elevation=weather["elevation"],
            update_time=update_time,
            update_interval=timedelta(seconds=interval_seconds),
            temperature=current["temperature_2m"],
            temperature_unit=current_units["temperature_2m"],
            humidity=current["relative_humidity_2m"],
            pressure=current["pressure_msl"],
            wind_speed=current["wind_speed_10m"],
            wind_bearing=current["wind_direction_10m"],
            condition_code=current["weathercode"],
            forecast=forecast_data,
        )


class ArednMeshWeatherError(Exception):
    """Base exception for the library."""


class CannotConnect(ArednMeshWeatherError):
    """Exception for when the client cannot connect."""


class InvalidData(ArednMeshWeatherError):
    """Exception for when the data is invalid."""
