# services/base.py
from abc import ABC, abstractmethod

class BaseService(ABC):

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def get(self, id: str):
        pass