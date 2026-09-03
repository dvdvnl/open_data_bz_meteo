import datetime

from open_data_bz_meteo import Sensor, Station
from open_data_bz_meteo.const import DATE_FORMAT

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
    "SCODE": "12345",
    "DESC_D": "Temperatur",
    "DESC_I": "Temperature",
    "DESC_L": "Temperatura",
    "TYPE": "LT",
    "UNIT": "C",
    "VALUE": "12.3",
    "DATE": "2023-01-01T12:00:00CET",
}


class TestSensor:
    def test_parse_aliases(self):
        """Ensure sensor model fields are populated via alias mapping."""

        sensor = Sensor.model_validate(SENSOR_SAMPLE)
        assert sensor.station_code == "12345"
        assert sensor.description_deu == "Temperatur"
        assert sensor.type == "LT"
        assert sensor.unit == "C"
        assert sensor.value == "12.3"
        assert sensor.date == "2023-01-01T12:00:00CET"

    def test_datetime_property(self):
        """Verify `parsed_datetime` parses the raw date string into a datetime."""

        sensor = Sensor.model_validate(SENSOR_SAMPLE)
        assert isinstance(sensor.parsed_datetime, datetime.datetime)
        assert sensor.parsed_datetime == datetime.datetime.strptime(
            SENSOR_SAMPLE["DATE"], DATE_FORMAT
        ).replace(tzinfo=datetime.UTC)

    def test_numeric_sensor_value(self):
        """Ensure numeric values are accepted for the sensor value field."""

        s = Sensor.model_validate({**SENSOR_SAMPLE, "VALUE": 5.6})
        assert s.value == 5.6


class TestStation:
    def test_parse_aliases(self):
        """Ensure station model fields are populated via alias mapping."""

        station = Station.model_validate(STATION_SAMPLE)
        assert station.station_code == "ABCDE"
        assert station.name_eng == "Station"

        # Coordinates should be parsed as floats
        assert station.latitude == 46.0
        assert station.longitude == 11.0

    def test_numeric_station(self):
        """Confirm numeric fields remain numeric after validation."""

        data = {**STATION_SAMPLE, "ALT": 205.57, "LONG": 11.20262, "LAT": 46.243333}
        station = Station.model_validate(data)
        assert isinstance(station.altitude, float)
        assert station.altitude == 205.57
        assert isinstance(station.longitude, float)
        assert station.longitude == 11.20262
        assert isinstance(station.latitude, float)
        assert station.latitude == 46.243333

    def test_sensor_methods(self):
        """Validate station sensor helpers: type listing and lookup."""

        station = Station.model_validate(STATION_SAMPLE)
        assert station.sensor_types == []

        # Attach fake sensors
        s1 = Sensor.model_validate(SENSOR_SAMPLE)
        s2 = Sensor.model_validate({**SENSOR_SAMPLE, "TYPE": "GS"})
        station.sensors = [s1, s2]
        assert station.sensor_types == ["LT", "GS"]
        assert station.get_sensor("GS") is s2
        assert station.get_sensor("XX") is None
