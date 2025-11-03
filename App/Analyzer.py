import Fetcher
import pandas

def get_dataframe():
    raw_data = Fetcher.fetch_csgoempire()
    if raw_data and "data" in raw_data:
        jsonDataArray = raw_data["data"]
        df_raw = pandas.DataFrame(jsonDataArray)
        
        # Keep only relevant columns
        df = df_raw[['market_name', 'auction_ends_at', 'purchase_price', 'price_is_unreliable', 'market_value']].copy()
        
        # Calculate the difference from market value
        df['above_market'] = df['purchase_price'] - df['market_value']
        
        return df
    return pandas.DataFrame()

def find_deals(df):
    if not df.empty:
        deals = df[(df['market_value'] > 200) & 
                   (df['above_market'] < -200) & 
                   (df['price_is_unreliable'] == False)]
        return deals
    return pandas.DataFrame()

        
    

    
