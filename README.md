# Open Data Client

Collection of Python API clients for different [Open Data](https://data.civis.bz.it) services. The services are provided by _Provincia autonoma di Bolzano - Informatica Alto Adige SPA_, its legal terms can be found [here](https://data.civis.bz.it/legal).

## Open Meteo Data

Client for the "Open Meteo Data V1" service, based on the [official documentation](https://data.civis.bz.it/dataset/misure-meteo-e-idrografiche).

| Class                | Description                                                                    |
| -------------------- | ------------------------------------------------------------------------------ |
| **OpenMeteoClient**  | Handles requests to the API and instanciates objects for stations and sensors. |
| **OpenMeteoStation** | Represents a station and its related data.                                     |
| **OpenMeteoSensor**  | Represents a single sensor and its data.                                       |
