from pydantic import BaseModel

class ParsedStation(BaseModel):
    address: str
    bsn: int
    standart_in_use: list[str]
    freq_in_use: dict[str, list[float]]
    standart_builders: list[str]
    freq_builders: dict[str, list[float]]