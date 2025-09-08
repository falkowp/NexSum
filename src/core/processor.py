from abc import ABC, abstractmethod
from typing import Dict, Any
from src.config.models import ProcessingResult

class BaseProcessor(ABC):
    """Abstract base class for all content processors"""
    
    @abstractmethod
    def process(self, text: str) -> ProcessingResult:
        pass
    
    @abstractmethod
    def can_process(self, content_type: str) -> bool:
        pass