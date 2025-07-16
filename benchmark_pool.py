import time
from sqlalchemy import create_engine

engine = create_engine(
    url = "postgresql://postgres:postgres@localhost:5432/trading",
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True, 
    pool_timeout=30
)

def bench_connections(n):
    start = time.perf_counter() ## performance counter
    for _ in range(n):
        with engine.connect() as conn: ## Each loop opens a connection using engine.connect()
            pass ## then closes with pass
    
    total = time.perf_counter() - start

    print(f"{n:>5} sequential connects/releases → {total:.3f}s ({total/n*1000:.3f} ms/op)")


if __name__ == "__main__":
    for count in (100,1000,5000):
        bench_connections(count)

