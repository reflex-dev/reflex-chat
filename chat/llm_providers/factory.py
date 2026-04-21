import os
from typing import Dict, Any, List
from .base import LLMProvider
from .openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider
from .google_provider import GoogleGenAIProvider


class LLMProviderFactory:
    """Factory class for creating LLM provider instances."""

    SUPPORTED_PROVIDERS = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "gemini": GoogleGenAIProvider,
    }

    @classmethod
    def create_provider(cls, provider_name: str = None) -> LLMProvider:
        """
        Create an LLM provider instance.

        Args:
            provider_name: Name of the provider (openai, ollama, google).
                         If None, uses LLM_PROVIDER environment variable or defaults to "openai".

        Returns:
            LLMProvider: Configured provider instance

        Raises:
            ValueError: If provider is not supported or configuration is invalid
        """
        if provider_name is None:
            provider_name = os.getenv("LLM_PROVIDER", "openai").lower()

        if provider_name not in cls.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider_name}. "
                f"Supported providers: {list(cls.SUPPORTED_PROVIDERS.keys())}"
            )

        provider_class = cls.SUPPORTED_PROVIDERS[provider_name]
        config = cls._get_provider_config(provider_name)

        provider = provider_class(config)
        validation_errors = provider.validate_config()
        if validation_errors:
            raise ValueError(
                f"Configuration errors for {provider_name}: {validation_errors}"
            )

        return provider

    @classmethod
    def _get_provider_config(cls, provider_name: str) -> Dict[str, Any]:
        """Get configuration for a specific provider from environment variables."""
        config = {}

        if provider_name == "openai":
            config = {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_MODEL"),
            }

        elif provider_name == "ollama":
            config = {
                "host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                "model": os.getenv("OLLAMA_MODEL"),
            }

        elif provider_name == "gemini":
            config = {
                "api_key": os.getenv("GEMINI_API_KEY"),
                "model": os.getenv("GEMINI_MODEL"),
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "location": os.getenv("GOOGLE_LOCATION", "us-central1"),
                "use_vertexai": os.getenv("GOOGLE_USE_VERTEXAI", "false").lower()
                == "true",
            }

        return config

    @classmethod
    def get_supported_providers(cls) -> List[str]:
        """Get list of supported provider names."""
        return list(cls.SUPPORTED_PROVIDERS.keys())
