import time
import asyncio ## simulate clients
import asyncpg
##from sqlalchemy import create_engine

'''
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

'''

async def bench_asyncpool(n, pool):
    start = time.perf_counter()

    async def one():
        async with pool.acquire(): ## conext manager
            pass
    
    await asyncio.gather(*[one() for _ in range(n)]) ## Return a future aggregating results // runs all connections concurrently
    total = time.perf_counter() - start 

    print(f"{n} concurrent acquires/releases → {total:.3f}s ({total/n*1000:.3f} ms/op)")

async def main():
    pool = await asyncpg.create_pool(
        dsn = "postgresql://postgres:postgres@localhost:5432/trading",
        min_size=5,
        max_size=15
    )

    await bench_asyncpool(100, pool)
    await bench_asyncpool(500, pool)
    await bench_asyncpool(5000, pool)
    await pool.close() ## waits till all connections all released thne suddenly closes conectionx
    
asyncio.run(main()) ## run the file


