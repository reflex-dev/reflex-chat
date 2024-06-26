import reflex as rx

from ..states.state import QA, State
from ..components import loading_icon


def create_message_item(text: rx.Component, shade: int, alignment: str):
    return rx.box(
        text,
        background_color=rx.color("mauve", shade),
        text_align=alignment,
        width="100%",
        padding="1em",
        border_radius="6px",
    )


def create_answer_options(path):
    return rx.button(
        rx.image(
            src=path,
            width="20px",
            height="20px",
            filter=rx.color_mode_cond(
                "invert(0)",
                "invert(1)",
            ),
        ),
        color_scheme="gray",
        variant="ghost",
        width="100%",
        justify_content="center",
        align_items="center",
    )


def message(qa: QA) -> rx.Component:
    """A single question/answer message.

    Args:
        qa: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.vstack(
        create_message_item(rx.text(qa.question), 2, "right"),
        rx.hstack(
            create_message_item(rx.text(qa.answer), 3, "left"),
            rx.vstack(
                create_answer_options("like.svg"),
                create_answer_options("dislike.svg"),
                create_answer_options("clipboard.svg"),
                border_radius="6px",
                justify_content="center",
                align_items="center",
                spacing="4",
            ),
            width="100%",
        ),
        width="100%",
        padding="1em",
        spacing="3",
    )


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
            spacing="3",
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
                        rx.radix.text_field.root(
                            rx.radix.text_field.input(
                                placeholder="Type something...",
                                id="question",
                                width=["15em", "20em", "45em", "50em", "50em", "50em"],
                            ),
                            rx.radix.text_field.slot(
                                rx.tooltip(
                                    rx.icon("info", size=18),
                                    content="Enter a question to get a response.",
                                )
                            ),
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
                # on_submit=State.process_question,
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
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('mauve', 3)}",
        background_color=rx.color("mauve", 2),
        align_items="stretch",
        width="100%",
    )
