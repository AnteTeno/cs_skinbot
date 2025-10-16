import fetcher
import json

raw_Data = fetcher.fetch_csgoempire()


def getneededInformation():
    jsonDataArray = raw_Data["data"]
    for item in jsonDataArray:
        suggested_price = item["suggested_price"]
        highest_bid = item["auction_highest_bid"]
        endsAt = item["auction_ends_at"]
        

    


