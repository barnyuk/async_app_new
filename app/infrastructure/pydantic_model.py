from pydantic import BaseModel, Field, field_validator, model_validator


from pydantic import BaseModel, Field, field_validator, model_validator

class SourceData(BaseModel):
    output_dir: str = Field(min_length=1)
    prev_prot_dir: str = Field(min_length=1)
    bsn_data: list[tuple[str, str]] = Field(min_length=1)
    start_protocol_number: str = Field(min_length=1)
    protocol_date: str = Field(min_length=1)
    measurements_date: str = Field(min_length=1)
    temperature: str | None = None
    humidity: str | None = None
    job_title: str = Field(min_length=1)
    generate_work_protocols: bool
    generate_final_protocols: bool
    is_builders: bool

    @field_validator(
        'output_dir', 'prev_prot_dir', 'start_protocol_number',
        'protocol_date', 'measurements_date',
        'job_title', 'temperature', 'humidity',
        mode='before'
    )
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator('start_protocol_number')
    @classmethod
    def validate_number(cls, v):
        if not v.isdigit():
            raise ValueError("Номер протокола должен состоять только из цифр")
        return v

    @field_validator('temperature', 'humidity')
    @classmethod
    def validate_numeric(cls, v):
        if v is None or v == "":
            return v
        try:
            float(v.replace(",", "."))
        except ValueError:
            raise ValueError("Ожидается число")
        return v

    @field_validator('bsn_data')
    @classmethod
    def validate_bsn_operators(cls, v):
        allowed = {'A1', 'BEST', 'BE_CLOUD'}
        
        for op, bsn_id in v:
            if op not in allowed:
                raise ValueError(f"Неизвестный оператор '{op}'. Допустимые: {', '.join(allowed)}")
            if not bsn_id:
                raise ValueError(f"У оператора {op} пустой BSN")
                
        if len(v) != len(set(v)):
            raise ValueError("Обнаружены дублирующиеся БС в списке")
            
        return v

    @model_validator(mode='after')
    def check_at_least_one_protocol_type(self):
        if not self.generate_work_protocols and not self.generate_final_protocols:
            raise ValueError("Выберите хотя бы один тип протоколов (рабочие или чистовые)")
        return self





