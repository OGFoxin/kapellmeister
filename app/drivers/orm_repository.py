from app.entities.models import TickerSchema,TickerModel
from app.interfaces.tickers import TickerRepository

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class ORMTickerRepository(TickerRepository):

    async def get_all_tickers(self, session: AsyncSession):
        return await self._get_all_tickers(session)

    async def add_ticker(self, ticker: TickerSchema, session: AsyncSession):
        return await self._add_ticker(ticker, session)

    async def get_ticker_by_name(self, session: AsyncSession, name: str):
        return await self._get_ticker_by_name(session, name)

    async def delete_ticker_by_name(self, session: AsyncSession, name: str):
        return await self._delete_ticker_by_name(session, name)

    async def _get_all_tickers(self,session: AsyncSession):
        try:
            query = select(TickerModel)
            result = await  session.execute(query)

            return result.scalars().all()

        except (TypeError, ValueError, IOError, InvalidRequestError) as e:
            return {"error": str(e), 'code': 500}

    async def _add_ticker(self, ticker: TickerSchema, session: AsyncSession):
        try:
            new_ticker = TickerModel(
                name=ticker.name,
                current_price=ticker.current_price,
            )
            session.add(new_ticker)
            await session.commit()

            return ticker

        except (TypeError, ValueError, IOError, InvalidRequestError) as e:
             return {"error": str(e), 'code': 500}

    async def _get_ticker_by_name(self, session: AsyncSession, name: str):
        try:
            query = select(TickerModel).where(TickerModel.name == name)
            result = await session.execute(query)
            ticker = result.scalars().first()

            if ticker is None:
                return {'message': f'Ticker with {name} not found', 'code': 404}

            return ticker

        except (TypeError, ValueError, IOError, InvalidRequestError) as e:
            return {"error": str(e), 'code': 500}

    async def _delete_ticker_by_name(self, session: AsyncSession, name: str):
        try:
            query = select(TickerModel).where(TickerModel.name == name)
            result = await session.execute(query)
            ticker = result.scalars().first()

            if ticker is None:
                return {'message': f'Ticker with name {name} not found', 'code': 404}

            await session.delete(ticker)
            await session.commit()

            return {'message': f'Ticker {name} successfully deleted', 'code': 200}

        except (TypeError, ValueError, IOError, InvalidRequestError) as e:
            return {"error": str(e), 'code': 500}


