##remember when doing tests just run functions from the soruce folder

from backend.src.ohlcv_binance import fetch_ohlcv, validate_ohlcv

def test_fetch_ohlcv():
    # testing the fetch_ohlcv function with a known symbol and interval
    df = fetch_ohlcv(symbol="BTCUSDT", interval="1d", start="2024-06-01", end="2024-06-10")
    assert len(df) > 0, "DataFrame should not be empty"
    assert {"open_time", "open", "high", "low", "close", "volume", "close_time"}.issubset(df.columns)
    validate_ohlcv(df)  # Validate the DataFrame structure and content

