import httpx
from .constants import URL_ENDPOINT, HEADERS

async def transform_maintenance_request(maintenance_request: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            data = {"message": maintenance_request}
            response = await client.post(URL_ENDPOINT, headers=HEADERS, json=data)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as exc:
        # Handle specific HTTP errors (4XX, 5XX)
        print(f"HTTP error occurred: {exc.response.status_code}")
    except httpx.RequestError as exc:
        # Handle request issues, like network errors
        print(f"An error occurred while requesting {exc.request.url!r}.")
    except Exception as exc:
        # Handle other unforeseen errors
        print(f"An error occurred: {exc}")