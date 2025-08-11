"""Class for a meteo sensor object"""

import datetime
from dataclasses import dataclass
from .const import DATE_FORMAT


@dataclass
class MeteoBzSensor:
    date: str
    description_deu: str
    description_ita: str
    description_lld: str
    station_code: str
    type: str
    unit: str
    value: str

    def __init__(self, apidata: dict[str, str]):

        # Set attributes
        self._data_to_attributes(apidata)

    # Convert API data to attributes
    def _data_to_attributes(self, apidata: dict[str, str]):
        self.station_code = apidata["SCODE"]

        # Sensor description
        self.description_deu = apidata["DESC_D"]
        self.description_ita = apidata["DESC_I"]
        self.description_lld = apidata["DESC_L"]

        # Sensor data
        self.type = apidata["TYPE"]
        self.unit = apidata["UNIT"]
        self.value = apidata["VALUE"]

        # Sensor measurement date
        self.date = apidata["DATE"]
        self.datetime = datetime.datetime.strptime(self.date, DATE_FORMAT)
