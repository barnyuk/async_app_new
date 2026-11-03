from app.infrastructure.api_models import ServerResponse
from app.infrastructure.mappers import map_to_stations


class HttpServerClient:
    # Метод теперь async!
    async def fetch_info(self, data: SourceData) -> list[ParsedStation]:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://api.server.com/data", json=data.model_dump())
            response.raise_for_status()
            
            raw_response = ServerResponse(**response.json())
            return map_to_stations(raw_response)