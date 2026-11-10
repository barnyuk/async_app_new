from collections import defaultdict

from app.infrastructure.api_model import ServerResponse
from app.infrastructure.parsed_model import ParsedStation


def process_stations(response: ServerResponse) -> list[ParsedStation]:

    stations = {}

    for feature in response.features:
        attr = feature.attributes
        bsn = attr.bsn

        # Если БС еще нет в словаре — создаем для нее "аккумулятор"
        if bsn not in stations:
            address = f"{attr.oblast} обл., {attr.district} р-н., н.п. {attr.city}, {attr.street}"
            stations[bsn] = {
                "address": address,
                "bsn": bsn,
                # Используем set() для стандартов, чтобы избежать дублей (LTE, LTE)
                "standart_in_use": set(),
                # Используем defaultdict(set) для частот, чтобы избежать дублей азимутов
                "freq_in_use": defaultdict(set),
                "standart_builders": set(),
                "freq_builders": defaultdict(set),
            }

        # Если БС уже есть, берем ее данные
        data = stations[bsn]

        # Распределяем данные в зависимости от статуса
        if attr.status == "Эксплуатация":
            data["standart_in_use"].add(attr.standart)
            data["freq_in_use"][attr.freq].add(attr.azimuth)
            
        elif attr.status == "Проектирование и строительство":
            data["standart_builders"].add(attr.standart)
            data["freq_builders"][attr.freq].add(attr.azimuth)

    # Превращаем сеты и defaultdict обратно в списки и обычные словари для Pydantic
    result = []
    for bsn, data in stations.items():
        result.append(ParsedStation(
            address=data["address"],
            bsn=data["bsn"],
            standart_in_use=sorted(list(data["standart_in_use"])),
            # Сортируем азимуты по возрастанию для красоты
            freq_in_use={k: sorted(list(v)) for k, v in data["freq_in_use"].items()},
            standart_builders=sorted(list(data["standart_builders"])),
            freq_builders={k: sorted(list(v)) for k, v in data["freq_builders"].items()},
        ))

    return result


