import reflex as rx

from ..states.state import QA, State
from ..components import loading_icon


def create_message_item(text: rx.Component, shade: int):
    return rx.box(
        text,
        background_color=rx.color("mauve", shade),
        width="100%",
        padding="12px 14px",
        border_radius="5px",
    )


def create_answer_options(path):
    return rx.button(
        rx.image(
            src=path,
            width="18px",
            height="18px",
            filter=rx.color_mode_cond(
                "invert(0)",
                "invert(1)",
            ),
        ),
        color_scheme="gray",
        variant="ghost",
        # width="100%",
        justify_content="center",
        align_items="center",
        cursor="pointer"
    )


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.

    """
    return rx.vstack(
        create_message_item(rx.text(qa.question, weight="medium", text_align="left"), 2),
        create_message_item(rx.markdown(qa.answer),1),
        rx.hstack(
            create_answer_options("like.svg"),
            create_answer_options("dislike.svg"),
            create_answer_options("clipboard.svg"),
            justify="end",
            align="center",
            width="100%",
            padding="10px",
        ),
        width="100%",
        spacing="1",
        font_family="Futura",
    )


def example_prompts(): ...

def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.vstack(
            rx.cond(
                State.is_hydrated & State.current_chat,
                rx.foreach(
                    State.chats[State.current_chat],
                    message,
                ),
                rx.spacer(),
            ),
            width="100%",
            spacing="9",
            padding="16px",
        ),
        flex="1",
        width="100%",
        max_width="50em",
        align_self="center",
        overflow="hidden",
        spacing="0",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.center(
        rx.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.hstack(
                        rx.input(
                            rx.input.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Enter a question to get a response.",
                                )
                            ),
                            placeholder="Type something...",
                            id="question",
                            width=["15em", "20em", "45em", "50em", "50em", "50em"],
                        ),
                        rx.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.text("Send"),
                            ),
                            type="submit",
                        ),
                        align_items="center",
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.process_question,
                reset_on_submit=True,
            ),
            rx.text(
                "ReflexGPT may return factually incorrect or misleading responses. Use discretion.",
                text_align="center",
                font_size=".75em",
                color=rx.color("mauve", 10),
            ),
            rx.logo(margin_top="-1em", margin_bottom="-1em"),
            align_items="center",
        ),
        position="sticky",
        bottom="0",
        left="0",
        padding_y="24px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        align_items="stretch",
        width="100%",
    )
