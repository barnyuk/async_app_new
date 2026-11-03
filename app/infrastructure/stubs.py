from app.models.models import ProtocolData
from app.infrastructure.pydantic_model import SourceData
from app.application.ports import ServerPort, DocxPort


class StubServer(ServerPort):
    def fetch_info(self, data: SourceData) -> list[dict]:
        print("[StubServer] Данные ушли на сервер, получаем ответ...")
        # Возвращаем фейковый ответ (типа сервер прислал 2 записи)
        return [{"bsn_id": "111", "op": "A1"}, {"bsn_id": "222", "op": "BEST"}]

class StubDocx(DocxPort):
    def generate(self, protocols: list[ProtocolData], output_dir: str) -> None:
        print(f"[StubDocx] Сохраняем {len(protocols)} протоколов в {output_dir}")
        for p in protocols:
            print(f"  - Номер: {p.protocol_number}, БСН: {p.bsn}, Тип: {p.protocol_type}")


