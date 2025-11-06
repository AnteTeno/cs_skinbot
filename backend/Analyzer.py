import Fetcher
import pandas
import Database
import logging

# Configure logging
logging.basicConfig(filename='analyzer_debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_dataframe(pages: int = 1):
    raw_data = Fetcher.fetch_csgoempire(pages=pages)
    if raw_data and "data" in raw_data:
        jsonDataArray = raw_data["data"]
        if not jsonDataArray:
            return pandas.DataFrame()
        df_raw = pandas.DataFrame(jsonDataArray)
        
        # Keep only relevant columns
        df = df_raw[['market_name', 'purchase_price', 'market_value', 'auction_ends_at']].copy()
        
        # Calculate discount percentage
        df['discount_percent'] = ((df['market_value'] - df['purchase_price']) / df['market_value']) * 100
        
        # Convert auction_ends_at to readable datetime in Finland timezone
        df['auction_ends_at'] = pandas.to_datetime(df['auction_ends_at'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/Helsinki')
        
        # Store data in database
        Database.insert_item_history(df[['market_name', 'purchase_price', 'market_value']])
        
        return df
    return pandas.DataFrame()

def get_historical_data(df):
    conn = Database.connect()
    market_names = tuple(df['market_name'].unique())

    # Use parameterized query to prevent SQL injection
    if len(market_names) == 0:
        conn.close()
        return pandas.DataFrame()

    placeholders = ','.join(['?' for _ in market_names])
    query = f"SELECT * FROM item_history WHERE market_name IN ({placeholders}) ORDER BY timestamp DESC"
    historical_df = pandas.read_sql_query(query, conn, params=market_names)
    conn.close()
    return historical_df

def calculate_trend(df):
    if not df.empty:
        df['moving_average'] = df.groupby('market_name')['purchase_price'].rolling(window=5, min_periods=1).mean().reset_index(level=0, drop=True)
    return df

def find_deals(df, min_discount=5):
    if not df.empty:
        historical_df = get_historical_data(df)
        if not historical_df.empty:
            historical_df = calculate_trend(historical_df)
            if not historical_df.empty:
                latest_trends = historical_df.groupby('market_name').last().reset_index()
                merged_df = pandas.merge(df, latest_trends[['market_name', 'moving_average']], on='market_name', how='left')
                deals = merged_df[(merged_df['purchase_price'] < merged_df['moving_average']) & (merged_df['discount_percent'] > min_discount)]
                return deals
    return pandas.DataFrame()

        
    

    
