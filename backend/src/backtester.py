##backtest logic

import numpy as np
import pandas as pd

def basic_strategy(df: pd.DataFrame) -> pd.DataFrame:
    '''## buy if close > prev_close, else flat
    df = df.copy()

    df["signal"] = (df["close"].diff() > 0).astype(int)
    df["signal"].iloc[0] = 0
    return df
    '''
    df = df.copy()
    ##long when todays close > yesterdays close
    df.loc[:, "signal"] = 0 ## create new colomn and intialise it to 0
    df.loc[df["close"] > df["close"].shift(1), "signal"] = 1 ##compares close price to prev close price
    ## if true set a signal
    df.loc[0, "signal"] = 0
    return df
    


def apply_slippage_and_commission( df: pd.DataFrame,
    slippage_bps: float = 5,
    commission_bps: float = 2
) -> pd.DataFrame:
    df = df.copy()

    slippage = (slippage_bps / 1000) * df["close"]
    commission = (commission_bps / 1000) * df["close"]

    ##assume buy on open of signal bar, sell on open of next
    df.iloc[:, "entry_price"] = df["close"] + slippage + commission
    return df
##pct_chnage computes the percentage change in price 
def compute_performance(
    df: pd.DataFrame,
    intial_capital: float = 1.0
                        ) -> tuple[dict, pd.DataFrame]:
    df = df.copy()
    #pos priior to singal
    df.iloc[:, "position"] = df["signal"].shift(1).fillna(0) ## enter next bar
    #daily returns
    df.iloc[:, "daily_returns"] = df["close"].pct_change().fillna(0)
    ##profit and lost
    df.iloc[:, "strategy_return "] = df["daily_returns"] * df["positions"]
    ##equity curve
    df.iloc[:, "equity"] = (1 + df["strategy_return"]).cumprod() * intial_capital

    return {
        "final_equity": float(df["equity"].iloc[-1]),
        "return_pct": float((df["equity"].iloc[-1] -1))*100,
        "max_drawdown": float(df["equity"].cummax() - df["equity"]).max(),
        "sharpe": float(
            df["strategy_return"].mean() / (df["strategy_return"].std() + 1e-8) * np.sqrt(252)),
        "trades": int(df["signal"].sum()),
    }, df

