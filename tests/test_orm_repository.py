import pytest
from unittest.mock import AsyncMock,patch
from app.drivers.orm_repository import ORMTickerRepository
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
def repository():
    return ORMTickerRepository()

@pytest.fixture
def mock_session():
    mock_session = AsyncMock(AsyncSession)
    return mock_session

@pytest.mark.all
@pytest.mark.asyncio
@pytest.mark.orm
async def test_add_new_ticker(repository, mock_session):
    mock_ticker = [
        {'id': 4, 'name': 'SOL', 'price': 500 },
    ]
    with patch.object(ORMTickerRepository,'_add_ticker', new_callable=AsyncMock) as mock_new_ticker:
        mock_new_ticker.return_value = mock_ticker

        actual_result = await repository.add_ticker(mock_ticker, mock_session)
        mock_new_ticker.assert_called_once_with(mock_ticker,mock_session)

    assert  actual_result == mock_ticker

@pytest.mark.all
@pytest.mark.asyncio
@pytest.mark.orm
async def test_get_all_tickers(repository, mock_session):
    mock_tickers = [
        {'id': 1, 'name': 'BTC', 'price': 100000 },
        {'id': 2, 'name': 'ETH', 'price': 3000   },
        {'id': 3, 'name': 'ADA', 'price': 10     },
        {'id': 4, 'name': 'SOL', 'price': 500    },
    ]
    with patch.object(ORMTickerRepository,'_get_all_tickers', new_callable=AsyncMock) as mock_get_all:
        mock_get_all.return_value = mock_tickers

        actual_result = await repository.get_all_tickers(mock_session)
        mock_get_all.assert_called_once_with(mock_session)

    assert actual_result == mock_tickers

@pytest.mark.all
@pytest.mark.asyncio
@pytest.mark.orm
async def test_delete_ticker(repository, mock_session):
    mock_ticker = [
        {'SOL'},
    ]
    with patch.object(ORMTickerRepository, '_delete_ticker_by_name', new_callable=AsyncMock) as mock_delete_ticker:
        mock_delete_ticker.return_value = mock_ticker

        actual_result = await repository.delete_ticker_by_name(mock_session, mock_ticker)
        mock_delete_ticker.assert_called_once_with(mock_session,mock_ticker)

    assert actual_result == mock_ticker
