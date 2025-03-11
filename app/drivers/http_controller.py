from app.drivers.orm_repository import ORMTickerRepository
from app.entities.models import Base,TickerSchema
from utils import get_tmp_db

import logging
from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import InvalidRequestError

router = APIRouter()
logger = logging.getLogger(__name__)
ticker = ORMTickerRepository()

# delete, only for local tests
engine = create_async_engine('sqlite+aiosqlite:///' + get_tmp_db())
new_async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

# temp
@router.post('/setup_database')
async def setup_database(self):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        return {"OK": True}
    except (TypeError, ValueError, IOError, InvalidRequestError) as e:
        return {"error": str(e), 'code': 500}

@router.get('/get_all_tickers')
async def get_all_tickers(session: SessionDep):
    return await ticker.get_all_tickers(session)

@router.post('/add_ticker')
async def add_ticker(tick: TickerSchema, session: SessionDep):
    return await ticker.add_ticker(tick,session)

@router.get('/get_ticker_by_name/{name}')
async def get_ticker_by_name(session: SessionDep, name: str):
    return await ticker.get_ticker_by_name(session, name)

@router.delete('/delete_ticker_by_name')
async def delete_ticker_by_name(session: SessionDep, name: str):
    return await ticker.delete_ticker_by_name(session, name)





