import requests
from dotenv import load_dotenv
import json
from typing import Any
import os
load_dotenv() 

def fetch_csgoempire(pages: int = 1, timeout: int = 10) -> Any:
    """
    Fetch items from CSGOEmpire API and return parsed JSON.
    Does NOT print. Raises RuntimeError on network/HTTP/parse errors.
    """
    all_data = []
    base_url = "https://csgoempire.com/api/v2/trading/items?per_page=100&has_stickers=no"
    api_key = os.getenv("CSGO_EMPIRE_API_KEY")
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + api_key
    }

    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}"
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            # Network error, timeout, or non-2xx status
            raise RuntimeError(f"Request to {url} failed: {exc}") from exc

        try:
            data = response.json()
            if "data" in data:
                all_data.extend(data["data"])
        except ValueError as exc:
            # Invalid JSON in response
            snippet = (response.text or "")[:1000]
            raise RuntimeError(f"Failed to parse JSON response. Response snippet: {snippet}") from exc

    return {"data": all_data}

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



