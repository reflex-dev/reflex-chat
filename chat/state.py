import os
from typing import Any, TypedDict
import reflex as rx
from chat.llm_providers import LLMProviderFactory, Message

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()


class QA(TypedDict):
    """A question and answer pair."""

    question: str
    answer: str


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    _chats: dict[str, list[QA]] = {
        "Intros": [],
    }

    # The current chat name.
    current_chat = "Intros"

    # Whether we are processing the question.
    processing: bool = False

    # Whether the new chat modal is open.
    is_modal_open: bool = False

    # LLM Provider configuration
    current_provider: str = os.getenv("LLM_PROVIDER", "openai")
    current_model: str = ""
    provider_error: str = ""
    _provider_instance = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize_provider()

    def _initialize_provider(self):
        """Initialize the LLM provider."""
        try:
            self._provider_instance = LLMProviderFactory.create_provider(
                self.current_provider
            )
            self.current_model = self._provider_instance.get_default_model()
            self.provider_error = ""
        except Exception as e:
            self.provider_error = str(e)
            self._provider_instance = None

    @rx.event
    def create_chat(self, form_data: dict[str, Any]):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        new_chat_name = form_data["new_chat_name"]
        self.current_chat = new_chat_name
        self._chats[new_chat_name] = []
        self.is_modal_open = False

    @rx.event
    def set_is_modal_open(self, is_open: bool):
        """Set the new chat modal open state.

        Args:
            is_open: Whether the modal is open.
        """
        self.is_modal_open = is_open

    @rx.var
    def selected_chat(self) -> list[QA]:
        """Get the list of questions and answers for the current chat.

        Returns:
            The list of questions and answers.
        """
        return (
            self._chats[self.current_chat] if self.current_chat in self._chats else []
        )

    @rx.event
    def delete_chat(self, chat_name: str):
        """Delete the current chat."""
        if chat_name not in self._chats:
            return
        del self._chats[chat_name]
        if len(self._chats) == 0:
            self._chats = {
                "Intros": [],
            }
        if self.current_chat not in self._chats:
            self.current_chat = list(self._chats.keys())[0]

    @rx.event
    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.event
    def set_new_chat_name(self, new_chat_name: str):
        """Set the name of the new chat.

        Args:
            new_chat_name: The name of the new chat.
        """
        self.new_chat_name = new_chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self._chats.keys())

    @rx.event
    async def process_question(self, form_data: dict[str, Any]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if not question:
            return

        async for value in self.llm_process_question(question):
            yield value

    @rx.event
    async def llm_process_question(self, question: str):
        """Process the question using the configured LLM provider."""
        try:
            # Check if provider is available
            if self._provider_instance is None:
                self.provider_error = "No LLM provider configured. Please check your environment variables."
                # Add error message to chat
                qa = QA(question=question, answer=f"Error: {self.provider_error}")
                self._chats[self.current_chat].append(qa)
                yield
                return

            # Add the question to the list of questions.
            qa = QA(question=question, answer="")
            self._chats[self.current_chat].append(qa)

            # Clear the input and start the processing.
            self.processing = True
            self.provider_error = ""
            yield

            # Build the messages for the provider.
            messages = self._build_messages()

            # Initialize provider if needed
            await self._provider_instance.initialize()

            # Stream the response from the provider
            async for chunk in self._provider_instance.stream_chat(
                messages=messages, model=self.current_model
            ):
                self._chats[self.current_chat][-1]["answer"] += chunk
                self._chats = self._chats  # Trigger reactivity
                yield

        except Exception as e:
            self.provider_error = f"LLM processing error: {str(e)}"
            # Add error message to the chat
            if self._chats[self.current_chat]:
                self._chats[self.current_chat][-1]["answer"] = f"Error: {str(e)}"
                self._chats = self._chats
            yield

        finally:
            # Toggle the processing flag.
            self.processing = False

    def _build_messages(self) -> list[Message]:
        """Build the message list from chat history."""
        messages = [
            Message(
                role="system",
                content="You are a friendly chatbot named Reflex. Respond in markdown.",
            )
        ]

        # Add conversation history
        for qa in self._chats[self.current_chat]:
            messages.append(Message(role="user", content=qa["question"]))
            if qa["answer"]:  # Only add assistant messages that have content
                messages.append(Message(role="assistant", content=qa["answer"]))

        # Remove the last empty assistant message (the one we're currently filling)
        if messages and messages[-1].role == "assistant" and not messages[-1].content:
            messages = messages[:-1]

        return messages
