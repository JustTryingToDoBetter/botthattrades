'''

This sets up the core time-series table with a daily chunking interval. 
Adjust chunk_time_interval as needed for your ingestion frequency.

'''

revision = "2000_create_market_data"
down_revision = None
branch_labels = None
depends_on = None



from alembic import op
import sqlalchemy as sa
from datetime import timedelta

'''
def chunk_time_interval(st, et, im):
    chunks = []
    curr_time = st
    while curr_time <= et:
        nxt_time = curr_time + timedelta(minutes=im)
        chunks.append((curr_time, min(nxt_time, et)))
        curr_time = nxt_time
    return chunks
    
'''


##create a table
def upgrade():
    op.create_table(
        'market_data',
        sa.Column('id', sa.BigInteger,  autoincrement=True),
        sa.Column('timestamp_utc', sa.TIMESTAMP(timezone=True), primary_key=True),
        sa.Column('symbol', sa.Text, nullable=False), 
        sa.Column('open', sa.Float, nullable=False),
        sa.Column('high', sa.Float, nullable=False),
        sa.Column('low', sa.Float, nullable=False),
        sa.Column('close', sa.Float, nullable=False),
        sa.Column('bid', sa.Float, nullable=True),
        sa.Column('ask', sa.Float, nullable=True),
        sa.Column('volume', sa.BigInteger, nullable=False)
    )
    ## hypertable
    op.execute(
    "SELECT create_hypertable("
    "  'market_data', "
    "  'timestamp_utc', "
    "  chunk_time_interval => INTERVAL '1 day', "
    "  if_not_exists => TRUE"
    ");"
)


def downgrade():
    op.execute("SELECT drop_hypertable('market_data', if_exists => TRUE)")
    op.drop_table('market_data')