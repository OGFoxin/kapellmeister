import asyncio
import os.path

from app.interfaces.config import ConfigInterface
from pathlib import Path
from yaml import YAMLError, safe_load

class AsyncFileConfig(ConfigInterface):
    def __init__(self, config_path: str, reload_interval: int = 5):
        self.config_file = Path(config_path)
        self.reload_interval = reload_interval
        self.last_modified = 0
        self._config = {}


    async def load_config(self):
        if not self.config_file.is_file():
            raise FileNotFoundError(f'Config file not found in current directory {self.config_file}')

        with open(self.config_file, 'r', encoding='utf-8') as file:
            try:
                self._config = safe_load(file)
                return self._config
            except YAMLError as e:
                raise ValueError(f'Error parsing YAML {e}')

    def get(self, key: str, default=None):
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    async def check_for_updates(self):
        # lmt - last_modified_time
        while True:
            lmt = os.path.getmtime(self.config_file)
            if lmt > self.last_modified:
                print("Configuration will be updated...")
                await self.load_config()
                self.last_modified = lmt
            await asyncio.sleep(self.reload_interval)


