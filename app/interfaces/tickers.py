from app.entities.models import TickerSchema

from abc import ABC,abstractmethod
from typing import TypeVar,Generic

T = TypeVar('T')

class TickerRepository(ABC):
    @abstractmethod
    async def add_ticker(self,ticker: TickerSchema, session: Generic[T]):
        pass

    @abstractmethod
    async def _add_ticker(self,ticker: TickerSchema, session: Generic[T]):
        pass

    @abstractmethod
    async def get_ticker_by_name(self,session: Generic[T], name: str):
        pass

    @abstractmethod
    async def _get_ticker_by_name(self, session: Generic[T], name: str):
        pass

    @abstractmethod
    async def delete_ticker_by_name(self,session: Generic[T], name: str):
        pass

    @abstractmethod
    async def _delete_ticker_by_name(self,session: Generic[T], name: str):
        pass

    @abstractmethod
    async def get_all_tickers(self,session: Generic[T]):
        pass

    @abstractmethod
    async def _get_all_tickers(self,session: Generic[T]):
        pass