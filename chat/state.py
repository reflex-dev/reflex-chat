"""
Summary of the Assistant API Documentation:

The Assistant API allows developers to create, manage, and interact with AI assistants using OpenAI's powerful language models. The API provides endpoints for creating assistants, managing threads, and handling messages. Key features include:

1. Creating Assistants: Developers can create assistants with specific instructions and tools. The assistants can be customized to perform various tasks and respond in a desired manner.

2. Managing Threads: The API supports creating and managing threads, which are used to organize conversations. Each thread can contain multiple messages exchanged between the user and the assistant.

3. Handling Messages: Developers can add messages to threads and receive responses from the assistant. The API supports streaming responses, allowing for real-time interaction with the assistant.

4. Event Handling: The API provides event handlers to manage different events during the interaction, such as text creation, text delta, and tool calls. This allows developers to handle and process events as they occur.

For more detailed information, please refer to the official documentation: https://platform.openai.com/docs/assistants/quickstart
"""

import os
import reflex as rx
from openai import OpenAI
from datetime import datetime

# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str
    timestamp: datetime = datetime.now()


DEFAULT_CHATS = {
    "Intros": [],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        model = self.openai_process_question

        async for value in model(question):
            yield value

    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {
                "role": "system",
                "content": "You are a friendly chatbot named Reflex. Respond in markdown.",
            }
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Create an assistant
        client = OpenAI()
        assistant = client.beta.assistants.create(
            name="Reflex Assistant",
            instructions="You are a friendly chatbot named Reflex. Respond in markdown.",
            tools=[],
            model="gpt-4o",
        )

        # Create a thread
        thread = client.beta.threads.create()

        # Add a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Create a run and stream the response
        from typing_extensions import override
        from openai import AssistantEventHandler

        class EventHandler(AssistantEventHandler):
            @override
            def on_text_created(self, text) -> None:
                print(f"\nassistant > ", end="", flush=True)

            @override
            def on_text_delta(self, delta, snapshot):
                print(delta.value, end="", flush=True)

            def on_tool_call_created(self, tool_call):
                print(f"\nassistant > {tool_call.type}\n", flush=True)

            def on_tool_call_delta(self, delta, snapshot):
                if delta.type == 'code_interpreter':
                    if delta.code_interpreter.input:
                        print(delta.code_interpreter.input, end="", flush=True)
                    if delta.code_interpreter.outputs:
                        print(f"\n\noutput >", flush=True)
                        for output in delta.code_interpreter.outputs:
                            if output.type == "logs":
                                print(f"\n{output.logs}", flush=True)

        try:
            with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id=assistant.id,
                instructions="Please address the user as Jane Doe. The user has a premium account.",
                event_handler=EventHandler(),
            ) as stream:
                for item in stream:
                    if hasattr(item.choices[0].delta, "content"):
                        answer_text = item.choices[0].delta.content
                        # Ensure answer_text is not None before concatenation
                        if answer_text is not None:
                            self.chats[self.current_chat][-1].answer += answer_text
                        else:
                            # Handle the case where answer_text is None, perhaps log it or assign a default value
                            # For example, assigning an empty string if answer_text is None
                            answer_text = ""
                            self.chats[self.current_chat][-1].answer += answer_text
                        self.chats = self.chats
                        yield
        except Exception as e:
            print(f"Error occurred: {e}")

        # Toggle the processing flag.
        self.processing = False
