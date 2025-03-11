from abc import ABC,abstractmethod
from typing import Any

class ConfigInterface(ABC):
    @abstractmethod
    async def load_config(self):
        pass

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    async def check_for_updates(self):
        pass