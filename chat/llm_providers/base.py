from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, List, Any
import asyncio


class Message:
    """Standardized message format for all providers."""

    def __init__(self, role: str, content: str):
        self.role = role  # "system", "user", or "assistant"
        self.content = content

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the provider (setup clients, validate configuration)."""
        pass

    @abstractmethod
    async def stream_chat(
        self, messages: List[Message], model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion response.

        Args:
            messages: List of Message objects representing conversation history
            model: Model name to use (optional, uses default if not provided)

        Yields:
            str: Response content chunks
        """
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        """Get the default model for this provider."""
        pass

    @abstractmethod
    def validate_config(self) -> List[str]:
        """
        Validate provider configuration.

        Returns:
            List[str]: List of validation errors, empty if valid
        """
        pass

    def convert_to_provider_format(
        self, messages: List[Message]
    ) -> List[Dict[str, str]]:
        """Convert standardized messages to provider-specific format."""
        return [msg.to_dict() for msg in messages]
