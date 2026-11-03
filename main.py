from app.infrastructure.pydantic_model import SourceData
from app.infrastructure.stubs import StubServer, StubDocx
from app.application.use_case import GenerateProtocolsUseCase

  
test_data = SourceData(
        output_dir="output",
        prev_prot_dir="prev",
        start_protocol_number = '1',
        bsn_data=[("A1", "123"), ("BEST", "456")],
        protocol_date="2023-10-27",
        measurements_date="2023-10-27",
        temperature = None,
        humidity = None,
        job_title = 'Инженер',
        generate_work_protocols = True,
        generate_final_protocols = False,
        is_builders = False
    )


use_case = GenerateProtocolsUseCase(StubServer(), StubDocx())
use_case.execute(test_data)