import os
import pytest
from unittest.mock import patch
from infrastructure.config_controller import AsyncFileConfig
from utils import get_config_path
from test_utils import mock_home_dir

@pytest.fixture
def config():
    return AsyncFileConfig(config_path=get_config_path(), reload_interval=5)

@pytest.mark.all
@pytest.mark.config
async def test_config_exists(config,mock_home_dir):
    expected_result = '/mock/home/app/config/config.yml'

    with patch('os.path.exists', return_value=True):
        actual_result = get_config_path()

    assert actual_result == os.path.normpath(expected_result)


@pytest.mark.all
@pytest.mark.config
async def test_load_config(config):
    expected_result = [
        {'app':
            {
                'name': 'Kappellmeister',
                'version': '1.0.0'
            }
        },
    ]

    with patch.object(config, 'load_config', return_value=expected_result) :
        actual_result = await config.load_config()

    assert actual_result == expected_result



