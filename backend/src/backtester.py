##backtest logic

import numpy as np
import pandas as pd

def basic_strategy(df):
    ## buy if close > prev_close, else flat
    df = df.copy()

    df["signal"] = (df["close"].diff() > 0).astype(int)
    df["signal"].iloc[0] = 0
    return df


def apply_slippage_and_commission(df, slippage_bps=5,commission_bps=2):
    df = df.copy()

    slippage = (slippage_bps / 1000) * df["close"]
    commission = (commission_bps / 1000) * df["close"]

    ##assume buy on open of signal bar, sell on open of next
    df["fill_price"] = df["close"] + np.where(df["signal"] > 0, slippage, 0) + commission
    return df
##pct_chnage computes the percentage change in price 
def compute_performance(df):
    df = df.copy()
    df["position"] = df["signal"].shift(1).fillna(0) ## enter next bar
    df["pnl"] = (df["close"].pct_change() * df["position"]).fillna(0)
    df["equity"] = (1 + df["pnl"]).cumprod()

    return {
        "final_equity": df["equity"].iloc[-1],
        "return_pct": (df["equity"].iloc[-1] -1)*100,
        "max_drawdown": (df["equity"].cummax() - df["equity"]).max(),
        "sharpe": df["pnl"].mean() / (df["pnl"].std() + 1e-8) * np.sqrt(252),
        "trades": int(df["signal"].fillna(0).sum()),
    }, df

