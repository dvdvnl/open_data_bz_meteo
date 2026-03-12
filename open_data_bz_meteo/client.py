from __future__ import annotations

from .sensor import Sensor
from .station import Station
from typing import Optional
import requests


class Client:
    def __init__(
        self,
        base_url: str = "https://daten.buergernetz.bz.it/services/meteo/v1",
        timeout: int = 10,
        session: Optional[requests.Session] = None,
    ) -> None:
        """Create a client.

        Args:
            base_url: Base URL of the Open Meteo Data service (no trailing slash).
            timeout: Default request timeout in seconds.
            session: Optional requests.Session for advanced usage / testing.
        """
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout

        self.stations: list[Station] = []
        self.sensors: list[Sensor] = []

    # Get all stations
    def get_stations(self) -> list[Station]:
        """Fetch all stations from the API and cache them in `self.stations`.

        Returns:
            list[Station]: All stations returned by the service.
        """

        # GET request to the API
        response = self.session.get(
            f"{self.base_url}/stations",
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json().get("features", [])

        # Rebuild station list to avoid duplicates
        self.stations = []
        for feature in data:
            station_props = feature.get("properties", {})
            self.stations.append(Station.model_validate(station_props))

        return self.stations

    # Get a single station
    def get_station(self, station_code: str) -> Optional[Station]:
        """Return the station matching `station_code`, refreshing the station list.

        Args:
            station_code: The station code to look up.

        Returns:
            Optional[Station]: The matched station, or None if not found.
        """

        # Get all stations
        self.get_stations()

        # Loop through stations and return the station with the given station_code
        for station in self.stations:
            if station.station_code == station_code:
                return station

    # Get sensors from station
    def get_sensors(self, station: Station) -> list[Sensor]:
        """Fetch sensors for a specific station.

        Args:
            station: The station to fetch sensors for.

        Returns:
            list[Sensor]: Sensors belonging to the station.
        """

        sensors: list[Sensor] = []

        # GET request to the API
        response = self.session.get(
            f"{self.base_url}/sensors",
            params={"station_code": station.station_code},
            timeout=self.timeout,
        )

        response.raise_for_status()

        # Get the data from the response
        data = response.json() or []

        # Loop through data and create sensor objects via pydantic
        for sensor_data in data:
            sensors.append(Sensor.model_validate(sensor_data))

        return sensors

    # Get a single sensor from a station
    def get_sensor(self, station: Station, sensor_type: str) -> Sensor:
        """Fetch a single sensor by type for a station.

        Args:
            station: The station to query.
            sensor_type: The sensor type code to retrieve.

        Raises:
            ValueError: If no sensor with the given type exists for the station.

        Returns:
            Sensor: The requested sensor.
        """

        # GET request to the API
        response = self.session.get(
            f"{self.base_url}/sensors",
            params={"station_code": station.station_code, "sensor_code": sensor_type},
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json() or []
        if not data:
            raise ValueError(
                f"No sensor found with type '{sensor_type}' for station '{station.station_code}'"
            )

        return Sensor.model_validate(data[0])
