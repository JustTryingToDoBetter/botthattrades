## ytets for cli commands

import subprocess
import os
import json
import pandas as pd
import pytest

BACKTEST_CMD = [
    "python",
    "-m",
    "backend.src.cli", 
    "backtest", 
    "--symbol", 
    "BTCUSDT", 
    "--start", 
    "2022-01-01", 
    "--end", 
    "2022-01-02", 
    "--export"
]

@pytest.mark.parametrize(
         ["fmt", "ext", "parser"],
    [
        ("csv",  ".csv",  pd.read_csv),
        ("json", ".json", lambda f: pd.read_json(f, orient="records")),
    ],
)

def test_backtest_outputs(tmp_path, fmt, ext, parser):
    output_file = tmp_path / f"BTCUSDT_2022-01-01_2022-01-02_backtest{ext}"
    cmd = BACKTEST_CMD + [fmt]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(os.getcwd())
    subprocess.run(cmd, cwd=tmp_path, env=env, check=True)
    assert output_file.exists()
    df = parser(output_file)
    assert "timestamp_utc" in df.columns
    assert "equity" in df.columns
    assert len(df) > 1
