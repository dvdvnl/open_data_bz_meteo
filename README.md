# Open Data BZ Meteo - API Client

Python API client for the "Open Meteo Data V1" service, provided by _Provincia autonoma di Bolzano - Informatica Alto Adige SPA_. The API documentation can be found [here](https://data.civis.bz.it/dataset/misure-meteo-e-idrografiche).

## Core classes

### `Client`

Main entrypoint to the API.

- `get_stations()` fetches all stations and caches them on the client.
- `get_station(station_code)` looks up a single station by code (refreshes cache).
- `get_sensors(station)` fetches sensors for a given station.
- `get_sensor(station, sensor_type)` fetches a single sensor and raises `ValueError` if not found.

### `Station`

- Represents a station with location data (`latitude`, `longitude`, `altitude`) and localized names (`name_deu`, `name_eng`, `name_ita`, `name_lld`).
- `sensor_types`: sensor types available at this station.
- `get_sensor(sensor_type)`: returns the first matching sensor or `None`.

### `Sensor`

- Represents a single sensor reading with `type`, `unit`, `value`, and `date`.
- `parsed_datetime`: computed `datetime` parsed from the raw `date` string.
- Localized description (`description_deu`, `description_ita`, `description_lld`).

## Usage

```python
from open_data_bz_meteo import Client

client = Client(timeout=5)

# List available stations
stations = client.get_stations()
print(stations[0].name_eng, stations[0].latitude)

# Fetch sensors for a single station
station = stations[0]
station.sensors = client.get_sensors(station)
print([s.type for s in station.sensors])

# Fetch a single sensor by type
sensor = client.get_sensor(station, "WT")
print(sensor.value, sensor.unit)
```
