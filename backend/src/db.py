import pytest
from sqlalchemy import create_engine, inspect

@pytest.fixture(scope="session")
def db_engine():

    url = "postgresql://postgres:postgres@localhost:5432/trading"
    engine = create_engine(url)
    yield engine
    engine.dispose()

def test_market_data_table_exists(db_engine):
    inspector = inspect(db_engine)
    tables = inspector.get_table_names()
    assert "market_data" in tables, f"expected 'market_data' table, found {tables}"