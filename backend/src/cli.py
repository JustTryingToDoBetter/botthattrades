import click
import pandas as pd
from sqlalchemy import text
from .db import engine
from .backtester import basic_strategy, apply_slippage_and_commission, compute_performance

##creates a new group
@click.group()
def tb():
    pass

##attaches a command to a group
@tb.command()
@click.option("--symbol", default="BTCUSDT") ## attches option to command
@click.option("--start", default='2022-01-01')
@click.option("--end", default='2023-01-01')
@click.option("--export", type=click.Choice(['csv', 'json']), default='csv')
def backtest(symbol, start, end, export):
    query = text("""
        SELECT timestamp_utc, open, high, low, close, volume
        FROM market_data
        WHERE symbol = :symbol
          AND timestamp_utc >= :start
          AND timestamp_utc < :end
        ORDER BY timestamp_utc
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn, params={"symbol": symbol, "start": start, "end": end})
    
    df = basic_strategy(df)
    df = apply_slippage_and_commission(df)
    metrics, df = compute_performance(df)
    filename = f"{symbol}_{start}_{end}_backtest.{export}"
    if export == 'csv':
        df.to_csv(filename, index=False)
    else:
        df.to_json(filename, orient='records', date_format='iso')
    
    click.echo(f"{filename}\nPerformance: {metrics}")

if __name__ == "__main__":
    tb()