
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.settings import settings

db_url = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@pgdb:{settings.postgres_port}/{settings.postgres_db}"
engine = create_async_engine(
    db_url,
    echo=True,
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
