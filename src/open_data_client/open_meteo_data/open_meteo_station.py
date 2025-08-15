"""Class for a meteo station object"""

from dataclasses import dataclass, field
from .open_meteo_sensor import OpenMeteoSensor
from typing import Optional


@dataclass
class OpenMeteoStation:
    altitude: str
    latitude: str
    longitude: str
    name_deu: str
    name_eng: str
    name_ita: str
    name_lld: str
    station_code: str

    sensors: list[OpenMeteoSensor] = field(default_factory=list)

    def __init__(self, apidata: dict[str, str]):
        # Set attributes
        self._data_to_attributes(apidata)

    # Convert API data to attributes
    def _data_to_attributes(self, apidata: dict[str, str]):
        self.station_code = apidata["SCODE"]

        # Station description
        self.name_deu = apidata["NAME_D"]
        self.name_eng = apidata["NAME_E"]
        self.name_ita = apidata["NAME_I"]
        self.name_lld = apidata["NAME_L"]

        # Geographical data
        self.altitude = apidata["ALT"]
        self.longitude = apidata["LONG"]
        self.latitude = apidata["LAT"]

    # Get sensor types from station
    @property
    def sensor_types(self) -> list[str]:
        if self.sensors == []:
            return []

        sensor_types: list[str] = []
        for sensor in self.sensors:
            sensor_types.append(str(sensor.type))

        return sensor_types

    # Add a sensor to the station
    def get_sensor(self, type: str) -> Optional[OpenMeteoSensor]:
        for sensor in self.sensors:
            if sensor.type == type:
                return sensor
