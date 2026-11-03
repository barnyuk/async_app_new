from app.models.models import ProtocolData
from app.infrastructure.pydantic_model import SourceData
from app.application.ports import ServerPort, DocxPort
import asyncio


class GenerateProtocolsUseCase:
    def __init__(self, server: ServerPort, docx: DocxPort):
        self.server = server
        self.docx = docx

    async def execute(self, data: SourceData) -> None:
        
        server_data = await self.server.fetch_info(data)
        
        protocols = []
        
        number = int(data.start_protocol_number)
        
        for item in server_data:

            protocols.append(ProtocolData(
                bsn=(item["op"], item["bsn_id"]),
                protocol_number=str(number),
                protocol_date=data.protocol_date,
                measurements_date=data.measurements_date,
                job_title=data.job_title,
                temperature=data.temperature,
                humidity=data.humidity
            ))
            number += 1

        if data.generate_work_protocols:
            self.docx.generate_work_protocol(protocols, data.output_dir)

        if data.generate_final_protocols:
            self.docx.generate_final_protocol(protocols, data.output_dir)

        