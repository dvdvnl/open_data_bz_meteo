from open_data_bz_meteo import Client, Sensor, Station
import pytest
import requests_mock

STATION_SAMPLE = {
    "SCODE": "ABCDE",
    "NAME_D": "Haltestelle",
    "NAME_E": "Station",
    "NAME_I": "Stazione",
    "NAME_L": "Staziun",
    "ALT": "500",
    "LONG": "11.0",
    "LAT": "46.0",
}

SENSOR_SAMPLE = {
    "SCODE": "ABCDE",
    "DESC_D": "Temperatur",
    "DESC_I": "Temperature",
    "DESC_L": "Temperatura",
    "TYPE": "LT",
    "UNIT": "C",
    "VALUE": "12.3",
    "DATE": "2023-01-01T12:00:00CET",
}


def test_get_stations_roundtrip(requests_mock: requests_mock.Mocker):
    """Ensure `get_stations` fetches and parses station list from the API."""

    client = Client()
    url = "https://daten.buergernetz.bz.it/services/meteo/v1/stations"
    requests_mock.get(url, json={"features": [{"properties": STATION_SAMPLE}]})

    stations = client.get_stations()
    assert isinstance(stations, list)
    assert len(stations) == 1
    station = stations[0]
    assert isinstance(station, Station)
    assert station.station_code == "ABCDE"
    assert station.name_deu == "Haltestelle"
    assert station.latitude == 46.0
    assert station.longitude == 11.0


def test_get_sensors_and_get_sensor(requests_mock: requests_mock.Mocker):
    """Ensure `get_sensors` and `get_sensor` return expected results and error on missing sensor."""

    client = Client()
    station = Station.model_validate(STATION_SAMPLE)

    sensor_url = "https://daten.buergernetz.bz.it/services/meteo/v1/sensors"
    requests_mock.get(sensor_url, json=[SENSOR_SAMPLE])

    # List of sensors
    sensors = client.get_sensors(station)
    assert len(sensors) == 1
    assert isinstance(sensors[0], Sensor)
    assert sensors[0].type == "LT"

    # Single sensor
    single = client.get_sensor(station, "LT")
    assert isinstance(single, Sensor)
    assert single.type == "LT"

    # Sensor doesn't exist on station
    requests_mock.get(sensor_url, json=[])
    with pytest.raises(ValueError):
        client.get_sensor(station, "XX")


def test_get_stations_empty(requests_mock: requests_mock.Mocker):
    """Verify get_stations returns an empty list and rebuilds cache on subsequent calls."""

    client = Client()
    url = "https://daten.buergernetz.bz.it/services/meteo/v1/stations"
    requests_mock.get(url, json={"features": []})

    # API doesn't return stations
    stations_empty = client.get_stations()
    assert stations_empty == []

    # API returns stations on subsequent call
    requests_mock.get(url, json={"features": [{"properties": STATION_SAMPLE}]})
    stations = client.get_stations()
    assert len(stations) == 1


def test_get_station_not_found(requests_mock: requests_mock.Mocker):
    """Return None when requested station code is not present in API response."""

    client = Client()
    url = "https://daten.buergernetz.bz.it/services/meteo/v1/stations"

    # Station with wrong code
    wrong_station = {**STATION_SAMPLE, "SCODE": "ZZZZZ"}
    requests_mock.get(url, json={"features": [{"properties": wrong_station}]})

    assert client.get_station("ABCDE") is None


def test_get_station_found(requests_mock: requests_mock.Mocker):
    """Return a Station object when the requested station code exists."""

    client = Client()
    url = "https://daten.buergernetz.bz.it/services/meteo/v1/stations"
    requests_mock.get(url, json={"features": [{"properties": STATION_SAMPLE}]})

    result = client.get_station("ABCDE")
    assert isinstance(result, Station)
    assert result.station_code == "ABCDE"


def test_get_sensors_empty(requests_mock: requests_mock.Mocker):
    """Return an empty sensor list when the API returns no sensors."""

    client = Client()
    station = Station.model_validate(STATION_SAMPLE)

    sensor_url = "https://daten.buergernetz.bz.it/services/meteo/v1/sensors"
    requests_mock.get(sensor_url, json=[])

    sensors = client.get_sensors(station)
    assert sensors == []
