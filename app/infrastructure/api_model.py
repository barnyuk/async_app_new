from pydantic import BaseModel
from example_json import data

from pydantic import BaseModel

class Attributes(BaseModel):
    oblast: str
    district: str
    city: str
    street: str
    bsn: int
    standart: str
    freq: str
    azimuth: float
    status: str

class Feature(BaseModel):
    attributes: Attributes

class ServerResponse(BaseModel):
    features: list[Feature]

class ServerResponseItem(BaseModel):
    features: list[dict]


d = ServerResponseItem(**data)

print(d.features[0].attributes.street)


