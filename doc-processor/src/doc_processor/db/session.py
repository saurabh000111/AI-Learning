from sqlalchemy.ext.asyncio import (  # pyright: ignore[reportMissingImports]
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from doc_processor.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
