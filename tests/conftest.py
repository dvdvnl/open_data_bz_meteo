import os
import pytest
import sys


root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root not in sys.path:
    sys.path.insert(0, root)


@pytest.fixture
def sample_station_data() -> dict:
    """Return a small dict mimicking a station API payload."""
    return {
        "SCODE": "ABCDE",
        "NAME_D": "Haltestelle",
        "NAME_E": "Station",
        "NAME_I": "Stazione",
        "NAME_L": "Staziun",
        "ALT": "500",
        "LONG": "11.0",
        "LAT": "46.0",
    }


@pytest.fixture
def sample_sensor_data() -> dict:
    """Return a small dict mimicking a sensor API payload."""
    return {
        "SCODE": "ABCDE",
        "DESC_D": "Temperatur",
        "DESC_I": "Temperature",
        "DESC_L": "Temperatura",
        "TYPE": "LT",
        "UNIT": "C",
        "VALUE": "12.3",
        "DATE": "2023-01-01T12:00:00CET",
    }
