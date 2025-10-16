import requests
from config import CSGOEMPIRE_API_KEY

def fetch_csgoempire():
    url = "https://csgoempire.com/api/v2/trading/auctions?per_page=10&page=1"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + CSGOEMPIRE_API_KEY
    }
    response = requests.get(url, headers=headers)
    print(response.text)


if __name__ == "__main__":
    fetch_csgoempire()