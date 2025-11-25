from typing import AsyncGenerator, List, Dict, Any
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from .base import LLMProvider, Message


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None

    async def initialize(self) -> None:
        """Initialize the OpenAI client."""
        if not self.config.get("api_key"):
            raise ValueError("OpenAI API key is required")

        self.client = OpenAI(api_key=self.config["api_key"])

    async def stream_chat(
        self, messages: List[Message], model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion from OpenAI.

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

        # Convert messages to OpenAI format
        openai_messages = self._convert_messages_to_openai_format(messages)

        try:
            # Create streaming chat completion
            stream = self.client.chat.completions.create(
                model=model,
                messages=openai_messages,
                stream=True,
            )

            # Stream the response
            for chunk in stream:
                if (
                    hasattr(chunk.choices[0].delta, "content")
                    and chunk.choices[0].delta.content is not None
                ):
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def get_default_model(self) -> str:
        """Get the configured OpenAI model."""
        model = self.config.get("model")
        if not model:
            raise ValueError("OPENAI_MODEL environment variable is required")
        return model

    def validate_config(self) -> List[str]:
        """Validate OpenAI configuration."""
        errors = []

        if not self.config.get("api_key"):
            errors.append("OPENAI_API_KEY environment variable is required")

        model = self.config.get("model")
        if not model:
            errors.append("OPENAI_MODEL environment variable is required")
        elif not isinstance(model, str):
            errors.append("OPENAI_MODEL must be a valid string")

        return errors

    def _convert_messages_to_openai_format(
        self, messages: List[Message]
    ) -> List[ChatCompletionMessageParam]:
        """Convert standardized Message objects to OpenAI format."""
        openai_messages = []

        for message in messages:
            openai_messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        return openai_messages
