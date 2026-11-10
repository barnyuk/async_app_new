import aiohttp
import asyncio
import requests
import keyring
# from app.settings.settings import APP_NAME

APP_NAME = 'protocol_app'



keyring.set_password(APP_NAME, username, password)


class HttpServerClient:

    # еще я должен получить токен))
    TOKEN_URL = 'https://xn--80atti9b.xn--80ad2a0b1c.xn--90ais/elitegis/tokens/generateToken/'
    TIMEOUT = 5

    def __init__(self, timeout_sec: int = 5, max_concurrent: int = 5):
        self.timeout = aiohttp.ClientTimeout(total=self.TIMEOUT)
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._token = self.token

    async def fetch_info(self, token: str, items: list[tuple[str, str]]) -> list[dict | None]:
        async with aiohttp.ClientSession(timeout=self.timeout) as session:

            tasks = [BsnTask(token, session, item, self.semaphore)() for item in items]
            
            results = await asyncio.gather(*tasks)
            
            return list(results)

    @property
    def token(self):
        username = keyring.get_password(APP_NAME, username, password)
        print(username)

        response = requests.post(
            self.TOKEN_URL,
            data={'username': username, 'password': password, 'f': 'json'},
            timeout=self.TIMEOUT,
        ).json()

        token = response.get('token') if isinstance(response, dict) else None
        
        if not isinstance(token, str) or not token:
            raise ValueError('Authentication failed: the service did not return a token.')

        return token

class BsnTask:

    MAP_URL = 'https://xn--80atti9b.xn--80ad2a0b1c.xn--90ais/elitegis/rest/services/TEST/Test1sl/MapServer/4/query'
    OPERATOR_MNC = {'A1': '1', 'BEST': '4', 'BE_CLOUD': '6'}

    def __init__(self, token: str, session: aiohttp.ClientSession, item: tuple[str, str], semaphore: asyncio.Semaphore):
        self.token = token
        self.session = session
        self.item = item
        self.semaphore = semaphore

    async def __call__(self) -> dict | None:
        # Семафор теперь ограничивает КАЖДЫЙ конкретный запрос
        async with self.semaphore:
            try:
                params = self.prepare_params(self.token, self.item)
                response = await self.session.get(self.MAP_URL, params=params)
                response.raise_for_status()
                print(response)
                # Возвращаем JSON, а не сам объект response!
                data = await response.json()                
                return data               
            
            except asyncio.TimeoutError:
                print(f"Таймаут для {self.item}")
                return None
            except aiohttp.ClientError as e:
                print(f"Ошибка сети для {self.item}: {e}")
                return None
            except Exception as e:
                print(f"Неизвестная ошибка для {self.item}: {e}")
                return None

    def prepare_params(self, token: str, item: tuple[str, str]) -> dict[str, str]:
        operator, bsn_id = item
        mnc = self.OPERATOR_MNC.get(operator)
        
        if mnc is None:
            raise ValueError(f"Неизвестный оператор: {operator}")

        return {
            'f': 'json',
            'token': token,
            'where': f"mnc = '{mnc}' AND bsn = '{bsn_id}'",
            'returnCountOnly': 'false',
            'outFields': '*',
        }


h = HttpServerClient()

print(h.get_token())