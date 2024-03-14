import os
import reflex as rx
from openai import OpenAI

_client = None


def get_openai_client():
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    return _client


assistant_id = os.getenv("ASSISTANT_ID")

PASSWORD = os.getenv("PASSWORD")

# Checking if the API key is set properly
if not os.getenv("OPENAI_API_KEY"):
    raise Exception("Please set OPENAI_API_KEY environment variable.")

# Checking if the assistant key is set properly
if not os.getenv("ASSISTANT_ID"):
    raise Exception("Please set ASSISTANT_ID environment variable.")


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": {"id": "", "messages": []},
}


class State(rx.State):
    """The app state."""

    password: str = ""

    correct_password: bool = False

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, dict[str, list[QA]]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    def check_password(self):
        if PASSWORD == self.password:
            self.correct_password = True
        else:
            return rx.window_alert("Invalid password.")

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = {"id": "", "messages": []}

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
        self.chats[self.current_chat]["messages"].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        if self.chats[self.current_chat]["id"] == "":
            thread = get_openai_client().beta.threads.create()
            self.chats[self.current_chat]["id"] = thread.id
        else:
            thread = get_openai_client().beta.threads.retrieve(
                thread_id=self.chats[self.current_chat]["id"]
            )

        get_openai_client().beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=qa.question,
        )

        run = get_openai_client().beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistant_id
        )

        # Periodically retrieve the Run to check status and see if it has completed
        while run.status != "completed":
            keep_retrieving_run = get_openai_client().beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

            if keep_retrieving_run.status == "completed":
                break

            if keep_retrieving_run.status == "failed":
                self.processing = False
                yield rx.window_alert("OpenAI Request Failed! Try asking again.")
                return

        # Retrieve messages added by the Assistant to the thread
        all_messages = get_openai_client().beta.threads.messages.list(
            thread_id=thread.id
        )

        answer_text = all_messages.data[0].content[0].text.value

        if answer_text is not None:
            self.chats[self.current_chat]["messages"][-1].answer += answer_text
        else:
            # Handle the case where answer_text is None, perhaps log it or assign a default value
            # For example, assigning an empty string if answer_text is None
            answer_text = ""
            self.chats[self.current_chat]["messages"][-1].answer += answer_text

        self.chats = self.chats
        yield

        # Toggle the processing flag.
        self.processing = False
