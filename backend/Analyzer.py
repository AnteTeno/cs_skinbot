import Fetcher
import pandas

import Database

def get_dataframe(pages: int = 1):
    raw_data = Fetcher.fetch_csgoempire(pages=pages)
    if raw_data and "data" in raw_data:
        jsonDataArray = raw_data["data"]
        if not jsonDataArray:
            return pandas.DataFrame()
        df_raw = pandas.DataFrame(jsonDataArray)
        
        # Keep only relevant columns
        df = df_raw[['market_name', 'purchase_price', 'market_value']].copy()
        
        # Store data in database
        Database.insert_item_history(df)
        
        return df
    return pandas.DataFrame()

def get_historical_data(market_name):
    conn = Database.connect()
    query = f"SELECT * FROM item_history WHERE market_name = '{market_name}' ORDER BY timestamp DESC LIMIT 100"
    df = pandas.read_sql_query(query, conn)
    conn.close()
    return df

def calculate_trend(df):
    if not df.empty:
        df['moving_average'] = df['purchase_price'].rolling(window=5).mean()
    return df

def find_deals(df, min_discount=5):
    if not df.empty:
        deals = df[(df['purchase_price'] < df['moving_average']) & 
                   (df['discount_percent'] > min_discount)]
        return deals
    return pandas.DataFrame()

        
    

    
