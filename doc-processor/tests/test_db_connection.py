import asyncio

from doc_processor.db.session import engine
from sqlalchemy import text


async def main() -> None:
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))

        print(result.scalar_one())

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
