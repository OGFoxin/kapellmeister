import logging
import os
import sys
from datetime import datetime, timezone

HOME_LOGS = 'app\\logs'
CURRENT_LOG = 'kapellmeister_current.log'
CONFIG_NAME = 'config.yml'

def get_config_path() -> str:
    return os.path.normpath(os.path.join(get_home_dir(),'app\\config',CONFIG_NAME))

def get_home_dir() -> str:
    return os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

# delete, only for local tests
def get_tmp_db() -> str:
    return get_home_dir() + '/infrastructure/db/tickers.db'

def create_current_log() -> str:
    try:
        if not os.path.exists(os.path.join(get_home_dir(), HOME_LOGS)):
            os.makedirs(os.path.join(get_home_dir(),HOME_LOGS))

        log_path = os.path.join(get_home_dir(), HOME_LOGS, CURRENT_LOG)
        return os.path.normpath(log_path)
    except (TypeError, ValueError, IOError) as e:
        return f'Error: {e}'

def close_loging_handler():
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

def rename_current_log() -> bool:
    close_loging_handler()
    try:
        os.rename(os.path.normpath(os.path.join(get_home_dir(), HOME_LOGS, CURRENT_LOG)),
                  os.path.normpath(os.path.join(get_home_dir(), HOME_LOGS, 'kapellmeister_'
                               + datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S') + '.log'))
                  )
        return True
    except (TypeError, ValueError, IOError) as e:
        print(f'ERROR: to rename current file {e}')
        return False

def write_log_iso_format():
    print(datetime.now().isoformat())

def is_unix_os() -> bool:
    if sys.platform.startswith("win"):
        return False