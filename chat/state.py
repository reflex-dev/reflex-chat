import os
from typing import Any, TypedDict
import reflex as rx
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


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

    # The name of the new chat.
    new_chat_name: str = ""

    @rx.event
    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self._chats[self.new_chat_name] = []

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
        if question == "":
            return

        async for value in self.openai_process_question(question):
            yield value

    @rx.event
    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self._chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "You are a friendly chatbot named Reflex. Respond in markdown.",
            }
        ]
        for qa in self._chats[self.current_chat]:
            messages.append({"role": "user", "content": qa["question"]})
            messages.append({"role": "assistant", "content": qa["answer"]})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        session = OpenAI().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            stream=True,
        )

        # Stream the results, yielding after every word.
        for item in session:
            if hasattr(item.choices[0].delta, "content"):
                answer_text = item.choices[0].delta.content
                # Ensure answer_text is not None before concatenation
                if answer_text is not None:
                    self._chats[self.current_chat][-1]["answer"] += answer_text
                else:
                    # Handle the case where answer_text is None, perhaps log it or assign a default value
                    # For example, assigning an empty string if answer_text is None
                    answer_text = ""
                    self._chats[self.current_chat][-1]["answer"] += answer_text
                self._chats = self._chats
                yield

        # Toggle the processing flag.
        self.processing = False
