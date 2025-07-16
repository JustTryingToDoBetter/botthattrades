## unit tetst for migradtions and db


import pytest
from sqlalchemy import inspect
from backend.src.db import engine

@pytest.fixture(scope="session")
def connection():
    conn = engine.connect()
    yield conn
    conn.close()

def test_market_data_table_exists(connection):
    inspector = inspect(connection)
    tables = inspector.get_table_names()
    assert "market_data" in tables