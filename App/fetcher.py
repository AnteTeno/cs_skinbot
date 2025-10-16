import requests
from config import CSGOEMPIRE_API_KEY
import json
from typing import Any

def fetch_csgoempire(timeout: int = 10) -> Any:
    """
    Fetch items from CSGOEmpire API and return parsed JSON.
    Does NOT print. Raises RuntimeError on network/HTTP/parse errors.
    """
    url = "https://csgoempire.com/api/v2/trading/items?per_page=10&page=1&auction=yes&has_stickers=no"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + CSGOEMPIRE_API_KEY
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Network error, timeout, or non-2xx status
        raise RuntimeError(f"Request to {url} failed: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        # Invalid JSON in response
        snippet = (response.text or "")[:1000]
        raise RuntimeError(f"Failed to parse JSON response. Response snippet: {snippet}") from exc

    return data

def format_json(data: Any, pretty: bool = True) -> str:
    """Return JSON string for printing/logging (caller decides when/where to print)."""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)

if __name__ == "__main__":
    try:
        data = fetch_csgoempire()
        # print(format_json(data))
    except RuntimeError as err:
        print(f"Error: {err}")



