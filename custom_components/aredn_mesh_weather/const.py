"""Constants for the AREDN Mesh Weather integration."""

DOMAIN = "aredn_mesh_weather"

DEFAULT_URL = "http://meshweather.local.mesh/?mode=data"

# Mapping from WMO weather codes to HA condition states
# See: https://www.home-assistant.io/integrations/weather/#condition-mapping
WMO_TO_HA_CONDITION = {
    0: "clear-night",
    1: "sunny",
    2: "partlycloudy",
    3: "cloudy",
    45: "fog",
    48: "fog",
    51: "rainy",
    53: "rainy",
    55: "rainy",
    61: "rainy",
    63: "rainy",
    65: "rainy",
    80: "rainy",
    81: "pouring",
    82: "pouring",
    95: "lightning-rainy",
    96: "lightning-rainy",
    99: "lightning-rainy",
    71: "snowy",
    73: "snowy",
    75: "snowy",
    77: "snowy",
    85: "snowy-rainy",
    86: "snowy-rainy",
}
