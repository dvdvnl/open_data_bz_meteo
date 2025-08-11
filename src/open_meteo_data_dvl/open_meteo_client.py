import requests
from typing import Optional

from .open_meteo_sensor import OpenMeteoSensor
from .open_meteo_station import OpenMeteoStation


class OpenMeteoClient:
    stations: list[OpenMeteoStation] = []
    sensors: list[OpenMeteoSensor] = []

    # Get all stations
    def get_stations(self) -> list[OpenMeteoStation]:
        # GET request to the API
        response = requests.get(
            "http://daten.buergernetz.bz.it/services/meteo/v1/stations"
        )

        # Get the data from the response
        data = response.json().get("features")

        # Loop through data and create a station objects
        for feature in data:
            station_data = feature["properties"]
            self.stations.append(OpenMeteoStation(station_data))

        return self.stations

    # Get a single station
    def get_station(self, station_code: str) -> Optional[OpenMeteoStation]:
        # Get all stations
        self.get_stations()

        # Loop through stations and return the station with the given station_code
        for station in self.stations:
            if station.station_code == station_code:
                return station

    # Get sensors from station
    def get_sensors(self, station: OpenMeteoStation) -> list[OpenMeteoSensor]:
        sensors: list[OpenMeteoSensor] = []

        # GET request to the API
        response = requests.get(
            "http://daten.buergernetz.bz.it/services/meteo/v1/sensors",
            params={"station_code": station.station_code},
        )

        # Get the data from the response
        data = response.json()

        # Loop through data and create a sensor objects
        for sensor_data in data:
            sensors.append(OpenMeteoSensor(sensor_data))

        return sensors

    # Get a single sensor from a station
    def get_sensor(self, station: OpenMeteoStation, type: str) -> OpenMeteoSensor:
        # GET request to the API
        response = requests.get(
            "http://daten.buergernetz.bz.it/services/meteo/v1/sensors",
            params={"station_code": station.station_code, "sensor_code": type},
        )

        data = response.json()
        if not data:
            raise ValueError(
                f"No sensor found with type '{type}' for station '{station.station_code}'"
            )

        return OpenMeteoSensor(data[0])
