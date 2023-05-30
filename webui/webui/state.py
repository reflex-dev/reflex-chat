import time

# import openai

# openai.api_key = "xxx"


import pynecone as pc


class State(pc.State):
    """The app state."""

    chats: dict[str, list[dict[str, str]]] = {
        "Intros": [{"question": "What is your name?", "answer": "Pynecone"}],
        "History paper": [
            {"question": "Can you help me on a history paper", "answer": "Sure!"}
        ],
    }
    models = ["Model1", "Model2", "Model3"]
    question: str
    current_chat = "Intros"
    current_model = "Model1"
    processing: bool = False
    new_chat_name: str = ""
    drawer_open: bool = False
    modal_open: bool = False

    def create_chat(self):
        self.chats[self.new_chat_name] = []
        self.current_chat = self.new_chat_name

    def toggle_modal(self):
        self.modal_open = not self.modal_open

    def toggle_processing(self):
        self.processing = not self.processing

    def set_chat(self, chat_id: str):
        self.current_chat = chat_id

    @pc.var
    def chat_title(self) -> list[str]:
        return list(self.chats.keys())

    def process_question(self):
        # response = openai.Completion.create(
        #     model="text-davinci-002",
        #     prompt=self.question,
        #     temperature=0,
        #     max_tokens=200,
        #     top_p=1,
        # )
        # answer = response["choices"][0]["text"].replace("\n", "")
        time.sleep(0.2)
        answer = "Hello there!"
        self.chats[self.current_chat].append(
            {"question": self.question, "answer": answer}
        )
        self.chats = self.chats
        return self.toggle_processing()

    def delete_chat(self):
        del self.chats[self.current_chat]
        self.current_chat = list(self.chats.keys())[0]

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open
