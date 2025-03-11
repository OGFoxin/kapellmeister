import logging
import uvicorn
from app.interfaces.config import ConfigInterface
from utils import create_current_log
from typing import Any

class ConfigReader:
    def __init__(self, config: ConfigInterface, app: Any):
        self.config = config
        self.app = app


    async def execute(self) -> tuple:
        await self.config.load_config()
        logging.basicConfig(filename=create_current_log(), level=self.config.get('logging.level', 'INFO'))

        config = uvicorn.Config(self.app, host=self.config.get('server.host', 'localhost'), port=self.config.get('server.port', '8080'),
                                reload=self.config.get('server.debug', 'False'))
        server = uvicorn.Server(config)
        logger = logging.getLogger(self.config.get('app.name', 'Default'))

        return server, logger

