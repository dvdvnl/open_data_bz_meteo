import datetime

from pydantic import BaseModel, Field, computed_field

from .const import DATE_FORMAT


class Sensor(BaseModel):
    """Represents a single sensor reading from the Open Meteo Data API.

    This model is created from API response records and provides a
    computed ``parsed_datetime`` property for easy datetime access.
    """

    date: str = Field(..., alias="DATE")
    description_deu: str = Field(..., alias="DESC_D")
    description_ita: str = Field(..., alias="DESC_I")
    description_lld: str = Field(..., alias="DESC_L")
    station_code: str = Field(..., alias="SCODE")
    type: str = Field(..., alias="TYPE")
    unit: str = Field(..., alias="UNIT")
    value: str | float = Field(..., alias="VALUE")

    @computed_field
    def parsed_datetime(self) -> "datetime.datetime":
        """Parsed :class:`datetime.datetime` from the raw ``date`` string."""
        return datetime.datetime.strptime(self.date, DATE_FORMAT).replace(
            tzinfo=datetime.UTC
        )
