from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Annotated
from sqlalchemy import select
import logging
from utils import get_tmp_db

router = APIRouter()

# delete, only for local tests
engine = create_async_engine('sqlite+aiosqlite:///' + get_tmp_db())
new_async_session = async_sessionmaker(engine, expire_on_commit=False)

logger = logging.getLogger(__name__)

async def get_session():
    async with new_async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

# alchemy
class TickerModel(Base):
    __tablename__ = 'tickers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

# pydentic
class TickerSchema(BaseModel):
    name: str

class TickerGetSchema(BaseModel):
    id: int

@router.post('/setup_database')
async def setup_database():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f'info: database setup')
        return {"OK": True}
    except (TypeError, ValueError, IOError, InvalidRequestError) as e:
        logger.error(f'error {e}')
        return {"error": str(e), 'code': 500}


@router.post('/add_ticker')
async def add_ticker(ticker: TickerSchema, session: SessionDep):
    try:
        new_ticker = TickerModel(
            name = ticker.name,
        )
        session.add(new_ticker)
        await session.commit()

        logger.info(f'info: {ticker.name}')

        return ticker
    except (TypeError, ValueError, IOError, InvalidRequestError) as e:
        logger.error(f'error {e}')
        return {"error": str(e), 'code': 500}

@router.get('/get_ticker_by_name/{name}')
async def get_ticker_by_name(session: SessionDep, name: str):
    try:
        query = select(TickerModel).where(TickerModel.name == name)
        result = await session.execute(query)
        ticker = result.scalars().first()

        if ticker is None:
            return {'message': f'Ticker with {name} not found', 'code': 404}

        return ticker
    except (TypeError, ValueError, IOError, InvalidRequestError) as e:
        logger.error(f'error {e}')
        return {"error": str(e), 'code': 500}


@router.get('/get_all_tickers')
async def get_all_tickers(session: SessionDep):
    try:
        query = select(TickerModel)
        result =  await  session.execute(query)
        return result.scalars().all()
    except (TypeError, ValueError, IOError, InvalidRequestError) as e:
        logger.error(f'error {e}')
        return {"error": str(e), 'code': 500}

@router.delete('/delete_ticker_by_name')
async def delete_ticker_by_name(session: SessionDep, name: str):
    try:
        query = select(TickerModel).where(TickerModel.name == name)
        result = await session.execute(query)

        if result.scalars().first() is None:
            return {'message': f'Ticker with name {name} not found', 'code': 404}

        await session.delete(result.scalars().first())
        await session.commit()

        return {'message': f'Ticker {name} successfully deleted', 'code': 200}
    except (TypeError, ValueError, IOError, InvalidRequestError) as e:
        logger.error(f'error {e}')
        return {"error": str(e), 'code': 500}