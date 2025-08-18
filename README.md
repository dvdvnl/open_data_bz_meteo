# Open Data Client

Collection of Python API clients for different [Open Data](https://data.civis.bz.it) services. The services are provided by _Provincia autonoma di Bolzano - Informatica Alto Adige SPA_, its legal terms can be found [here](https://data.civis.bz.it/legal).

## Open Meteo Data

Client for the "Open Meteo Data V1" (`p_bz:metereological_and_hydrographic_measurements`) API, based on the [official documentation](https://data.civis.bz.it/dataset/misure-meteo-e-idrografiche). Data is available in german, italian, and ladin.

| Class                | Description                                                                    |
| -------------------- | ------------------------------------------------------------------------------ |
| **OpenMeteoClient**  | Handles requests to the API and instanciates objects for stations and sensors. |
| **OpenMeteoStation** | Represents a station and its related data.                                     |
| **OpenMeteoSensor**  | Represents a single sensor and its data.                                       |

## Weatherservice

Client for the "Weatherservice" (`p_bz:southtyrolean-weatherservice-weathersouthtyrol`) API, based on the [official documentation](https://data.civis.bz.it/dataset/southtyrolean-weatherservice-weathersouthtyrol). Data is available in english, german, italian, and ladin.
