import fetcher
import json
import pandas

raw_Data = fetcher.fetch_csgoempire()


def getDataFrame():
    jsonDataArray = raw_Data["data"]
    df_raw = pandas.DataFrame(jsonDataArray)
    

    #Remove redundant data from dataframe
    df = df_raw[['market_name','auction_ends_at'
                , 'purchase_price', 'price_is_unreliable'
                ,'market_value']]
    
    #Add 'Is above market value?' to data frame
    df['above_market'] = df['purchase_price'] - df['market_value']

    find_deals(df)


def find_deals(df):
    if(df['market_value'] > 200 and df['above_market'] < -200 
       and df['price_is_unreliable'] == 0):
        
    

    
        

    


