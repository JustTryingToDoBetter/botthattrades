import requests
import pandas as pd
from datetime import datetime

BINANCE_URL = "https://api.binance.com/api/v3/klines"
# Fetch OHLCV data from Binance API
def fetch_ohlcv(symbol="BTCUSDT", interval="1d", start=None, end=None, limit=1000):
    # Construct the request parameters
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    ## Convert start and end dates to milliseconds since epoch
    if start:
        params["startTime"] = int(datetime.strptime(start, "%Y-%m-%d").timestamp() * 1000)
    if end:
        params["endTime"] = int(datetime.strptime(end, "%Y-%m-%d").timestamp() * 1000)

    resp = requests.get(BINANCE_URL, params=params) # Make the API request
    resp.raise_for_status()  # Raise an error for bad responses

    data = resp.json()  # Parse the JSON response
    # Convert the data into a DataFrame
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    # Convert timestamp to datetime and set as index
    df["open_time"] = pd.to_datetime(df["open_time"], unit='ms', utc=True)
    df["close_time"] = pd.to_datetime(df["close_time"], unit='ms', utc=True)
    
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors='coerce') # Convert price and volume columns to numeric
    df = df[["open_time", "open", "high", "low", "close", "volume", "close_time"]]  # Keep only relevant columns

    return df

def validate_ohlcv(df):
    #check for gaps in the data
    if df.empty:
        raise ValueError("No data returned from Binance API.")
    if df["open_time"].isnull().any():
        raise ValueError("Open time contains null values.")
    if df["close"].isnull().any():
        raise ValueError("Close prices contain null values.")
    if df["volume"].isnull().any():
        raise ValueError("Volume contains null values.")
    if not pd.api.types.is_datetime64_any_dtype(df["open_time"]):
        raise ValueError("Open time is not in datetime format.")