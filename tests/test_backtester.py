'''
tests fir backtester metrics 
porfi and loss
drawdown calculations

'''

import pandas as pd
from backend.src.backtester import basic_strategy, compute_performance, apply_slippage_and_commission

def test_backtester_metrics():
    ##minimal data

    df = pd.DataFrame({
        'close': [101, 102, 103, 105, 107],
    })

    df = basic_strategy(df)
    df = apply_slippage_and_commission(df, slippage_bps=0.01, commission_bps=0.001)
    metrics, df = compute_performance(df)

    assert metrics["final_equity"] > 0, "Final equity should be greater than 0"
    assert metrics["trades"] >= 1

