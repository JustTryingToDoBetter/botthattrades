##createnig a pool connection
##creating an engine with queuepool

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

##queuepool
engine = create_engine(
    url = 'postgresql://postgres:postgres@localhost:5432/trading', 
    pool_size=5, ##connection size
    max_overflow=10, ## until cut out
    pool_timeout = 30, ## seconds
    pool_pre_ping= True ##validate stale connnections
)
## setsup a factory fpor cretaing sessions to conenct to the db
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

