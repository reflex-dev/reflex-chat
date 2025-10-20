from typing import AsyncGenerator, List, Dict, Any
import asyncio
from .base import LLMProvider, Message


class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation for local models.

    Default options applied to all requests:
    - num_ctx: 4096 (context window size)
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None

    async def initialize(self) -> None:
        """Initialize the Ollama client."""
        try:
            # Import ollama here to avoid import errors if not installed
            import ollama

            self.client = ollama.Client(
                host=self.config.get("host", "http://localhost:11434")
            )
        except ImportError:
            raise ImportError(
                "Ollama package is not installed. Install it with: pip install ollama"
            )
        except Exception as e:
            raise Exception(
                f"Failed to connect to Ollama at {self.config.get('host')}: {str(e)}"
            )

    async def get_available_models(self) -> List[str]:
        """Get list of available local Ollama models."""
        if self.client is None:
            await self.initialize()

        try:
            # Run in thread pool to avoid blocking
            models = await asyncio.get_event_loop().run_in_executor(
                None, self.client.list
            )
            return [model["name"] for model in models.get("models", [])]
        except Exception:
            # If API call fails, return empty list - user must specify model manually
            return []

    async def stream_chat(
        self, messages: List[Message], model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion from Ollama.

        Args:
            messages: List of Message objects
            model: Model name to use

        Yields:
            str: Response content chunks
        """
        if self.client is None:
            await self.initialize()

        if model is None:
            model = self.get_default_model()

        # Convert messages to Ollama format
        ollama_messages = self._convert_messages_to_ollama_format(messages)

        # Default options with context size set to 4096
        default_options = {"num_ctx": 4096}

        try:
            # Use AsyncClient for streaming
            import ollama

            async_client = ollama.AsyncClient(
                host=self.config.get("host", "http://localhost:11434")
            )

            # Stream the response with default options
            async for chunk in await async_client.chat(
                model=model,
                messages=ollama_messages,
                stream=True,
                options=default_options,
            ):
                if chunk.get("message", {}).get("content"):
                    yield chunk["message"]["content"]

        except Exception as e:
            # Fallback to sync client if async fails
            try:
                stream = self.client.chat(
                    model=model,
                    messages=ollama_messages,
                    stream=True,
                    options=default_options,
                )
                for chunk in stream:
                    if chunk.get("message", {}).get("content"):
                        yield chunk["message"]["content"]
            except Exception as fallback_error:
                raise Exception(
                    f"Ollama streaming error: {str(e)} (fallback: {str(fallback_error)})"
                )

    def get_default_model(self) -> str:
        """Get the configured Ollama model."""
        model = self.config.get("model")
        if not model:
            raise ValueError("OLLAMA_MODEL environment variable is required")
        return model

    def validate_config(self) -> List[str]:
        """Validate Ollama configuration."""
        errors = []

        host = self.config.get("host", "http://localhost:11434")
        if not host:
            errors.append(
                "OLLAMA_HOST must be a valid URL (defaults to http://localhost:11434)"
            )

        model = self.config.get("model")
        if not model:
            errors.append("OLLAMA_MODEL environment variable is required")
        elif not isinstance(model, str):
            errors.append("OLLAMA_MODEL must be a valid string")

        return errors

    async def health_check(self) -> bool:
        """Check if Ollama is accessible and has models."""
        try:
            await self.initialize()
            models = await self.get_available_models()
            return len(models) > 0
        except Exception:
            return False

    def _convert_messages_to_ollama_format(
        self, messages: List[Message]
    ) -> List[Dict[str, str]]:
        """Convert standardized Message objects to Ollama format."""
        ollama_messages = []

        for message in messages:
            # Ollama supports the same format as OpenAI
            ollama_messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        return ollama_messages
