from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMBase(ABC):
    """Base class for LLM implementations"""
    
    @abstractmethod
    def generate(self, prompt: str, context: str = None) -> str:
        """Generate response from the LLM"""
        pass

class LLMException(Exception):
    """Custom exception for LLM-related errors"""
    pass
