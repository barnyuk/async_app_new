from dataclasses import dataclass


@dataclass(frozen=True)
class ProtocolData:
    address: str
    bsn: tuple[str, str]
    protocol_number: str
    protocol_date: str 
    measurements_date: str
    job_title: str 
    standart: list
    freq: dict
    standart_in_use: list[str]
    tandart_in_use: list[str]
    freq_in_use: dict[str, list[float]]
    standart_builders: list[str]
    freq_builders: dict[str, list[float]]
    temperature: str | None = None
    humidity: str | None = None

    
    

