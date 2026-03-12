"""A small CLI demonstrating usage of the Client and models."""

from open_data_bz_meteo import Client
from typing import Optional


def select_station_code(client: Client) -> Optional[str]:
    """Ask the user to pick a station from the list or enter a custom code."""
    stations = client.get_stations()
    if not stations:
        print("No stations available from the API.")
        return None

    print("Available stations:")
    for idx, st in enumerate(stations):
        print(f"{idx}: {st.station_code} – {st.name_eng}")

    choice = input("Select a number or type a station code: ").strip()
    if choice.isdigit():
        idx = int(choice)
        if 0 <= idx < len(stations):
            return stations[idx].station_code
        print("Index out of range.")
        return None

    return choice or None


def display_station_data(code: str) -> None:
    client = Client()
    station = client.get_station(code)
    if station is None:
        print(f"Station with code '{code}' not found.")
        return

    # obtain sensors and attach them to the station model
    station.sensors = client.get_sensors(station)

    print("---")
    print(
        f"{station.name_eng} {station.altitude}m ({station.station_code})",
        f"last update {station.sensors[0].parsed_datetime if station.sensors else 'N/A'}",
    )

    for sensor in station.sensors:
        print(f"{sensor.description_deu}: {sensor.value} {sensor.unit} ({sensor.type})")

    # show two example lookups
    for sensor_type in ("LT", "GS"):
        try:
            s = client.get_sensor(station, sensor_type)
        except ValueError:
            continue
        print(f"specific {sensor_type}: {s.value}{s.unit} – {s.description_deu}")


if __name__ == "__main__":
    client = Client()
    code = select_station_code(client)
    if code:
        display_station_data(code)
