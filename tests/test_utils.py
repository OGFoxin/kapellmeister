import os
import pytest
from unittest.mock import patch
from utils import create_current_log,rename_current_log,write_log_iso_format
from datetime import datetime

@pytest.fixture
def mock_home_dir():
    with patch('utils.get_home_dir', return_value='/mock/home') as home_dir:
        yield home_dir

@pytest.fixture
def mock_rename():
    with patch('os.rename') as mock_rename:
        yield mock_rename

@pytest.mark.all
@pytest.mark.utils
def test_create_current_log_success(mock_home_dir):
    with patch('os.path.exists', return_value=False), patch('os.makedirs'):
        actual_result = create_current_log()
        expected_result = '/mock/home/app/logs/kapellmeister_current.log'

        assert actual_result == os.path.normpath(expected_result)

@pytest.mark.all
@pytest.mark.utils
def test_create_current_log_exists(mock_home_dir):
    with patch('os.path.exists', return_value=True):
        actual_result = create_current_log()
        expected_result = '/mock/home/app/logs/kapellmeister_current.log'

        assert actual_result == os.path.normpath(expected_result)

@pytest.mark.all
@pytest.mark.utils
def test_rename_current_log_success(mock_home_dir, mock_rename):
    with patch('os.path.exists', return_value=True):
        with patch('utils.datetime') as mock_date_time:
            mock_date_time.now.return_value = datetime(2023, 10, 1, 12, 0, 0)
            mock_create_log = create_current_log()
            mock_rename_log = '/mock/home/app/logs/kapellmeister_20231001_120000.log'

            actual_result = rename_current_log()

            mock_rename.assert_called_once_with(
                os.path.normpath(mock_create_log),
                os.path.normpath(mock_rename_log)
            )

        assert actual_result is True

@pytest.mark.all
@pytest.mark.utils
def test_write_log_iso_format(capsys):
    mock_datetime = '2025-02-16T12:00:00.121211'

    with patch('utils.datetime') as mock_date_format:
        mock_date_format.now.return_value = datetime.fromisoformat(mock_datetime)

        write_log_iso_format()
        captured = capsys.readouterr()

        assert captured.out.strip() == mock_datetime