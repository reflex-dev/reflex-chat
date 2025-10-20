from typing import AsyncGenerator, List, Dict, Any
import asyncio
from .base import LLMProvider, Message


class GoogleGenAIProvider(LLMProvider):
    """Google GenAI provider implementation for Gemini models."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None

    async def initialize(self) -> None:
        """Initialize the Google GenAI client."""
        try:
            from google import genai
        except ImportError:
            raise ImportError(
                "Google GenAI package is not installed. Install it with: pip install google-genai"
            )

        if not self.config.get("api_key"):
            raise ValueError("Google API key is required")

        # Initialize client based on configuration
        if self.config.get("use_vertexai", False):
            # Use Vertex AI
            if not self.config.get("project_id"):
                raise ValueError("Google project ID is required for Vertex AI")

            self.client = genai.Client(
                vertexai=True,
                project=self.config["project_id"],
                location=self.config.get("location", "us-central1"),
                api_key=self.config["api_key"],
            )
        else:
            # Use Developer API
            self.client = genai.Client(api_key=self.config["api_key"])

    async def get_available_models(self) -> List[str]:
        """Get list of available Google Gemini models."""
        if self.client is None:
            await self.initialize()

        try:
            # Try to get models from the API if available
            # Note: Google GenAI may not have a public list models API
            # For now, return empty list - user must specify model manually
            return []
        except Exception:
            return []

    async def stream_chat(
        self, messages: List[Message], model: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completion from Google GenAI.

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

        # Convert messages to Google format
        gemini_messages = self._convert_messages_to_gemini_messages(messages)

        try:
            # Use async client for streaming
            async with self.client.aio as aclient:
                response = await aclient.models.generate_content(
                    model=model,
                    contents=gemini_messages,
                )

                # Stream the response
                if hasattr(response, "text"):
                    # If response is complete, yield all at once
                    yield response.text
                else:
                    # Try to stream if available
                    async for chunk in response:
                        if hasattr(chunk, "text") and chunk.text:
                            yield chunk.text

        except Exception as e:
            # Fallback to sync client
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=gemini_messages,
                )
                if hasattr(response, "text"):
                    yield response.text
            except Exception as fallback_error:
                raise Exception(
                    f"Google GenAI streaming error: {str(e)} (fallback: {str(fallback_error)})"
                )

    def get_default_model(self) -> str:
        """Get the configured Google GenAI model."""
        model = self.config.get("model")
        if not model:
            raise ValueError("GEMINI_MODEL environment variable is required")
        return model

    def validate_config(self) -> List[str]:
        """Validate Google GenAI configuration."""
        errors = []

        if not self.config.get("api_key"):
            errors.append("GEMINI_API_KEY environment variable is required")

        if self.config.get("use_vertexai", False):
            if not self.config.get("project_id"):
                errors.append("GOOGLE_PROJECT_ID is required when using Vertex AI")

        model = self.config.get("model")
        if not model:
            errors.append("GEMINI_MODEL environment variable is required")
        elif not isinstance(model, str):
            errors.append("GEMINI_MODEL must be a valid string")

        return errors

    def _convert_messages_to_gemini_messages(
        self, messages: List[Message]
    ) -> List[str]:
        """
        Convert standardized Message objects to Google GenAI format.

        Google GenAI uses a simpler content format where each message is a string.
        We'll combine system messages with user messages.
        """
        gemini_messages = []
        system_message = ""

        # Extract system message
        for message in messages:
            if message.role == "system":
                system_message = message.content
                break

        # Build conversation history
        for i, message in enumerate(messages):
            if message.role == "system":
                continue  # Skip system messages here
            elif message.role == "user":
                content = message.content
                if system_message and i == 0:
                    # Add system message to first user message
                    content = f"{system_message}\n\n{content}"
                gemini_messages.append(content)
            elif message.role == "assistant":
                gemini_messages.append(f"Assistant: {message.content}")

        return gemini_messages
