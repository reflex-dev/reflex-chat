"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import pynecone as pc
from .utils import navbar, sidebar
from .styles import *

import openai

openai.api_key = "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"


class State(pc.State):
    """The app state."""
    chats: dict[str, list[dict[str, str]]] = {
        "Chat1": [{"question": "What is your name?", "answer": "Pynecone"}],
        "Chat2": [{"question": "What is your age?", "answer": "1"}],
    }
    models: list[str] = ["Model1", "Model2", "Model3"]
    question: str
    current_chat = "Chat1"
    current_model = "Model1"
    processing: bool = False
    show: bool = False
    new_chat_name: str = ""

    def create_chat(self):
        self.chats[self.new_chat_name] = []
        self.current_chat = self.new_chat_name
        self.change()

    def change(self):
        self.show = not (self.show)

    def toggle_processing(self):
        self.processing = not self.processing

    def set_chat(self, chat_id: str):
        self.current_chat = chat_id

    @pc.var
    def chat_title(self) -> list[str]:
        return list(self.chats.keys())

    def process_question(self):
        print(self.question)
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.question,
            temperature=0,
            max_tokens=200,
            top_p=1,
        )
        answer = response["choices"][0]["text"].replace("\n", "")
        self.chats[self.current_chat].append(
            {"question": self.question, "answer": answer}
        )
        self.chats = self.chats
        self.toggle_processing()


def show_chat(qa):
    return pc.box(
        pc.box(
            pc.text(
                qa["question"],
                bg=accent_color,
                border="0.1em solid rgba(234,234,234, 1)",
                display="inline-block",
                padding=".75em",
                border_radius="5px",
            ),
            text_align="left",
        ),
        pc.box(
            pc.text(
                qa["answer"],
                bg=green_color,
                color="white",
                display="inline-block",
                padding=".75em",
                border_radius="5px",
            ),
            text_align="right",
            margin_top="1em",
        ),
        width="100%",
    )


class LoadingIcon(pc.Component):
    library = "react-loading-icons"
    tag = "ThreeDots"
    stroke: pc.Var[str]
    stroke_opacity: pc.Var[str]
    fill: pc.Var[str]
    fill_opacity: pc.Var[str]
    stroke_width: pc.Var[str]
    speed: pc.Var[str]

    @classmethod
    def get_controlled_triggers(cls) -> dict[str, pc.Var]:
        return {"on_change": pc.EVENT_ARG}
loading_icon = LoadingIcon.create

def middle(State):
    return pc.flex(
        pc.hstack(
            pc.heading(State.current_chat, text_align="left"),
            pc.spacer(),
            pc.box(
                pc.icon(tag="edit"),
                padding = ".5em",
                border = "0.1em solid rgba(234,234,234, 1)",
                border_radius="5px",
            ),
            pc.box(
                pc.icon(tag="delete"),
                padding = ".5em",
                border = "0.1em solid rgba(234,234,234, 1)",
                border_radius="5px",
            ),
            width = "100%",
            padding_bottom = "1em",
        ),
        pc.divider(),
        pc.vstack(
            pc.foreach(State.chats[State.current_chat], show_chat),
            padding_y="1em",
            spacing="1em",
            max_height = "100%",
            overflow_y = "scroll",
        ),
        pc.spacer(),
        pc.cond(
            State.processing,
            pc.center(
                loading_icon(
                    stroke=green_color,
                    fill=green_color,
                    stroke_width="1.5em",
                    speed=".5",
                    height="1em",
                ),
                padding_y="1em",
            )
        ),
        pc.vstack(
            pc.divider(),
            pc.hstack(
                pc.icon(tag="edit"),
                pc.icon(tag="edit"),
                pc.icon(tag="edit"),
                pc.icon(tag="edit"),

            ),
            pc.input_group(
                pc.input(
                    id="input1",
                    placeholder="Type something...",
                    on_blur=State.set_question,
                ),
                pc.input_right_addon(
                    pc.icon(tag="arrow_right"),
                    on_click=[State.toggle_processing, State.process_question],
                    bg="white",
                ),
            ),
            pc.text("This is a chat app that lets you chat with other users."),
        ),
        position="fixed",
        height="100%",
        top="0px",
        z_index=1,
        padding_left=["2em", "2em", "2em", "25em", "25em"],
        padding_right=["2em", "2em", "2em", "5em", "5em"],
        width="100%",
        padding_top="8em",
        padding_bottom="5em",
        text_align="center",
        flex_direction="column",
        bg="white",
    )


def index() -> pc.Component:
    return pc.center(
        navbar(State),
        pc.hstack(sidebar(State), middle(State), width="100%", padding_top="5em"),
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()