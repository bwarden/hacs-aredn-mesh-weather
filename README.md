# AREDN Mesh Weather Integration for Home Assistant

[![GitHub Release](https://img.shields.io/github/v/release/bwarden/hacs-aredn-mesh-weather?style=flat-square)](https://github.com/bwarden/hacs-aredn-mesh-weather/releases)
[![HACS Default](https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat-square)](https://github.com/bwarden/hacs-aredn-mesh-weather)
[![License](https://img.shields.io/github/license/bwarden/hacs-aredn-mesh-weather?style=flat-square)](LICENSE)

A custom Home Assistant integration designed to ingest meteorological data and metrics from your local **AREDN** (Amateur Radio Emergency Data Network) mesh weather nodes.

---

## Installation

### Method 1: Automated via HACS (Recommended)
Click the badge below to open this repository directly inside your Home Assistant instance via HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bwarden&repository=hacs-aredn-mesh-weather&category=integration)

Alternatively, you can add it manually:
1. Open **HACS** in your Home Assistant UI.
2. Click the three dots (`⋮`) in the top right corner and select **Custom repositories**.
3. Paste the URL: `https://github.com/bwarden/hacs-aredn-mesh-weather`
4. Select category: **Integration**.
5. Click **Add**, then search for and install **AREDN Mesh Weather**.
6. Restart Home Assistant.

### Method 2: Manual Installation
1. Download the `hacs-aredn-mesh-weather` folder from the [latest release](https://github.com/bwarden/hacs-aredn-mesh-weather/releases).
2. Copy the `custom_components/aredn_weather` directory into your Home Assistant configuration directory (`/config/custom_components/`).
3. Restart Home Assistant.

---

## Configuration

1. Once installed and restarted, navigate to **Settings** → **Devices & Services**.
2. Click **Add Integration** in the bottom right.
3. Search for **AREDN Mesh Weather** and select it.
4. Enter your mesh node's IP address/hostname and polling parameters when prompted.

---

## Entities & Sensors

This integration automatically provisions sensors for monitoring local mesh weather node telemetry, which may include:
* Temperature & Relative Humidity
* Barometric Pressure
* Wind Speed, Direction, and Gusts
* Node Link Quality and System Metrics

---

## Support & Contributing

If you encounter issues, have feature requests, or want to contribute to the code, please open an [Issue](https://github.com/bwarden/hacs-aredn-mesh-weather/issues) or submit a Pull Request on GitHub.
