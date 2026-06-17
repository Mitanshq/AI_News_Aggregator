import logging 
from abc import ABC, abstractmethod
from typing import Any
from services.gemini import gemini_client

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self):
        self.ai_service = gemini_client
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    async def process(self, content: str, *args, **kwargs):
        pass
