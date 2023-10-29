from pydantic import BaseModel

class CityModel(BaseModel):
    name: str


class CityOutput(BaseModel):
    id: int
    name: str
    weather: float
