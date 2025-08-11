from src.open_meteo_data_dvl.meteo_bz_client import MeteoBzClient


# List of strings to choose from
scodes = ["Custom", "83200MS", "27100MS", "23200MS", "35100WS"]
snames = ["", "Bolzano", "Gargazon", "Meran", "Jaufenkamm"]

# ask user to change one of the options
print("Choose a station code to get data from:")

for i in range(len(scodes)):
    print(str(i) + ": " + scodes[i], snames[i])

try:
    choice = int(input("Choose a number: "))
except ValueError:
    print("Invalid choice.")
    exit()

# Prompt for custom station code
if choice == 0:
    scode: str = input("Enter a station code: ")

    # Exit if no station code is provided
    if scode == "":
        print("Must provide station code.")
        exit()

# Choice is in range
elif choice >= 0 and choice < len(scodes):
    scode: str = scodes[choice]

# Choice is out of range
else:
    print("Invalid choice.")
    exit()

# Get station data
station = MeteoBzClient().get_station(scode)

if station is not None:
    # Get sensor data
    station.sensors = MeteoBzClient().get_sensors(station)

    # Print data
    print("---")
    print(
        f"{station.name_eng} {station.altitude}m ({station.station_code}) {station.sensors[0].datetime}:"
    )

    for sensor in station.sensors:
        print(f"{sensor.description_deu}: {sensor.value} {sensor.unit} ({sensor.type})")

    # Specific Sensor
    print("---")
    sensorLT = MeteoBzClient().get_sensor(station, "LT")
    print(
        f"{sensorLT.description_deu}: {sensorLT.value} {sensorLT.unit} ({sensorLT.type})"
    )

    sensorGS = MeteoBzClient().get_sensor(station, "GS")
    print(
        f"{sensorGS.description_deu}: {sensorGS.value} {sensorGS.unit} ({sensorGS.type})"
    )
