import time
import openai
import pynecone as pc
openai.api_key = "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"

class State(pc.State):
    """The app state."""

    chats: dict[str, list[dict[str, str]]] = {
        "Intros": [{"question": "What is your name?", "answer": "Pynecone"}],
    }
    question: str
    current_chat = "Intros"
    processing: bool = False
    new_chat_name: str = ""
    drawer_open: bool = False
    modal_open: bool = False

    def create_chat(self):
        self.chats[self.new_chat_name] = [{"question": "What is your name?", "answer": "Pynecone"}]
        self.current_chat = self.new_chat_name

    def rename_chat(self):
        self.chats[self.new_chat_name] = self.chats[self.current_chat]
        del self.chats[self.current_chat]
        self.current_chat = self.new_chat_name

    def toggle_modal(self):
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = {"New Chat": [{"question": "What is your name?", "answer": "Pynecone"}]}
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_id: str):
        self.current_chat = chat_id
        self.toggle_drawer()

    @pc.var
    def chat_title(self) -> list[str]:
        return list(self.chats.keys())

    
    async def process_question(self, form_data: dict) -> str:
        """Get the response from the API."""
        # Check if we have already asked the last question or if the question is empty
        self.question = form_data["question"]
        if self.chats[self.current_chat][-1]["question"] == self.question or self.question == "":
            return
        self.processing = True
        yield
        session = openai.Completion.create(
            engine='text-davinci-003',
            prompt=self.question,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
            stream=True  # Enable streaming
        )
        self.chats[self.current_chat].append({"question": self.question, "answer": ""})
        for item in session:
            answer_text = item['choices'][0]['text']
            self.chats[self.current_chat][-1]["answer"] += answer_text
            self.chats = self.chats
            yield

        self.processing = False
