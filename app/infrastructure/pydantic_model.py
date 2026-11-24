from pydantic import BaseModel, Field, field_validator, model_validator


class SourceData(BaseModel):
    output_dir: str = Field(min_length=1)
    prev_prot_dir: str = Field(min_length=1)
    bsn_data: list[tuple[str, str]] = Field(min_length=1)
    start_protocol_number: str
    protocol_date: str = Field(min_length=1)
    measurements_date: str = Field(min_length=1)
    temperature: str | None = None
    humidity: str | None = None
    job_title: str = Field(min_length=1)
    generate_work_protocols: bool
    generate_final_protocols: bool
    is_builders: bool

    @field_validator(
        "output_dir",
        "prev_prot_dir",
        "start_protocol_number",
        "protocol_date",
        "measurements_date",
        "job_title",
        "temperature",
        "humidity",
        mode="before",
    )
    @classmethod
    def strip_strings(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("start_protocol_number")
    @classmethod
    def validate_number(cls, v):
        if not v.isdigit():
            raise ValueError("Номер протокола должен состоять только из цифр")
        return v

    @field_validator("temperature", "humidity")
    @classmethod
    def validate_numeric(cls, v):
        if v is None or v == "":
            return None
        try:
            normalized = v.replace(",", ".")
            float(normalized)
        except ValueError as err:
            raise ValueError("Ожидается число") from err
        return normalized

    @model_validator(mode="after")
    def validate_protocols_requirements(self):
        if not self.generate_work_protocols and not self.generate_final_protocols:
            raise ValueError("Выберите хотя бы один тип протоколов (рабочие или чистовые)")
        if self.generate_final_protocols:
            if self.temperature is None:
                raise ValueError("Введите температуру")
            if self.humidity is None:
                raise ValueError("Введите влажность")
        return self
