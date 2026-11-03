from typing import Protocol
from app.models.models import ProtocolData
from app.infrastructure.pydantic_model import SourceData


class ServerPort(Protocol):
    
    def get_data_from_maps(self, data: SourceData) -> list[dict]:
        pass


class DocxPort(Protocol):
    
    def generate_work_protocol(self, protocols: list[ProtocolData], output_dir: str) -> None:
        pass

    def generate_final_protocol(self, protocols: list[ProtocolData], output_dir: str) -> None:
        pass

