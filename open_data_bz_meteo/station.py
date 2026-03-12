from .sensor import Sensor
from pydantic import BaseModel, Field, computed_field, ConfigDict
from typing import List, Optional


class Station(BaseModel):
    """Represents a meteorological station in the Open Meteo Data API.

    This model includes location data, localized station names, and an optional
    list of sensors that can be populated via the API client.
    """

    altitude: float = Field(..., alias="ALT")
    latitude: float = Field(..., alias="LAT")
    longitude: float = Field(..., alias="LONG")
    name_deu: str | None = Field(..., alias="NAME_D")
    name_eng: str | None = Field(..., alias="NAME_E")
    name_ita: str | None = Field(..., alias="NAME_I")
    name_lld: str | None = Field(..., alias="NAME_L")
    sensors: List[Sensor] = Field(default_factory=list)
    station_code: str = Field(..., alias="SCODE")

    @computed_field
    def sensor_types(self) -> List[str]:
        """Return a list of sensor types available at this station."""
        return [sensor.type for sensor in self.sensors] if self.sensors else []

    def get_sensor(self, sensor_type: str) -> Optional[Sensor]:
        """Return the first sensor matching `sensor_type`, or `None` if not found."""
        for sensor in self.sensors:
            if sensor.type == sensor_type:
                return sensor
