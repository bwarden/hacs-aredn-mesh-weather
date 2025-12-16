"""Parser for AREDN Mesh Weather data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


class InvalidData(Exception):
    """Raised when the data is invalid."""


@dataclass
class ArednMeshWeatherData:
    """AREDN Mesh Weather data."""

    # Current weather
    condition_code: int | None
    temperature: float | None
    temperature_unit: str | None
    pressure: float | None
    humidity: float | None
    wind_speed: float | None
    wind_bearing: float | None
    apparent_temperature: float | None
    cloud_cover: int | None
    wind_gust_speed: float | None
    precipitation: float | None

    # Forecasts
    forecast_daily: list[dict[str, Any]]
    forecast_hourly: list[dict[str, Any]]

    # Air Quality
    aqi: int | None
    pm25: float | None

    # NWS Alerts
    alerts: list[dict[str, Any]]

    # Meta
    update_time: datetime
    update_interval: timedelta

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ArednMeshWeatherData:
        """Parse data from the API."""
        try:
            if data.get("status") != "ok" or "weather" not in data:
                raise InvalidData("Weather data not found or status not ok")

            weather = data["weather"]
            current = weather["current"]
            daily = weather["daily"]
            hourly = weather["hourly"]
            air = data.get("air", {})
            air_hourly = air.get("hourly", {})
            nws_alerts = data.get("nws_alerts", {})

            # Find current hourly air quality index
            now = datetime.fromisoformat(current["time"])
            aqi = None
            pm25 = None
            if "time" in air_hourly and "us_aqi" in air_hourly:
                try:
                    current_air_index = air_hourly["time"].index(
                        now.strftime("%Y-%m-%dT%H:00")
                    )
                    aqi = air_hourly["us_aqi"][current_air_index]
                    pm25 = air_hourly["pm2_5"][current_air_index]
                except (ValueError, IndexError):
                    pass  # No current AQI data

            return cls(
                condition_code=current.get("weathercode"),
                temperature=current.get("temperature_2m"),
                temperature_unit=weather.get("current_units", {}).get("temperature_2m"),
                pressure=current.get("pressure_msl"),
                humidity=current.get("relative_humidity_2m"),
                wind_speed=current.get("wind_speed_10m"),
                wind_bearing=current.get("wind_direction_10m"),
                apparent_temperature=current.get("apparent_temperature"),
                cloud_cover=current.get("cloudcover"),
                wind_gust_speed=current.get("wind_gusts_10m"),
                precipitation=current.get("precipitation"),
                forecast_daily=[
                    {
                        "datetime": dt,
                        "condition": daily["weathercode"][i],
                        "temperature": daily["temperature_2m_max"][i],
                        "templow": daily["temperature_2m_min"][i],
                        "precipitation": daily["precipitation_sum"][i],
                        "wind_speed": daily["wind_speed_10m_max"][i],
                        "wind_bearing": daily["wind_direction_10m_dominant"][i],
                    }
                    for i, dt in enumerate(daily["time"])
                    if datetime.fromisoformat(dt).date() >= now.date()
                ],
                forecast_hourly=[
                    {
                        "datetime": dt,
                        "condition": hourly["weathercode"][i],
                        "temperature": hourly["temperature_2m"][i],
                        "precipitation": hourly["precipitation"][i],
                        "wind_speed": hourly["wind_speed_10m"][i],
                        "wind_bearing": hourly["wind_direction_10m"][i],
                    }
                    for i, dt in enumerate(hourly["time"])
                    if datetime.fromisoformat(dt) >= now
                ],
                aqi=aqi,
                pm25=pm25,
                alerts=nws_alerts.get("features", []),
                update_time=datetime.fromisoformat(current["time"]),
                update_interval=timedelta(seconds=current.get("interval", 900)),
            )
        except (KeyError, TypeError, IndexError) as exc:
            raise InvalidData from exc
