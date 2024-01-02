import reflex as rx

from webui import styles
from webui.components import loading_icon
from webui.state import QuestionAnswer, State


def message(question_answer: QuestionAnswer) -> rx.Component:
    """A single question/answer message.

    Args:
        question_answer: The question/answer pair.

    Returns:
        A component displaying the question/answer pair.
    """
    return rx.box(
        rx.box(
            rx.text(
                question_answer.question,
                bg=styles.border_color,
                shadow=styles.shadow_light,
                **styles.message_style,
                text_align="left",
            ),
            text_align="right",
            margin_top="1em",
        ),
        rx.box(
            rx.text(
                question_answer.answer,
                bg=styles.accent_color,
                shadow=styles.shadow_light,
                **styles.message_style,
            ),
            text_align="left",
            padding_top="1em",
        ),
        width="100%",
    )


def processing_message() -> rx.Component:
    """A message indicating that the maintenance request is being processed."""
    return rx.box(
        rx.box(
            rx.hstack(
                loading_icon(color="white", height="2em", width="1em"),
                rx.text("Processing your maintenance request..."),
            ),
            shadow=styles.shadow_light,
            **styles.message_style,
            text_align="left",
            margin_top="1em",
            bg="#538F88",
        )
    )


def submitted_message() -> rx.Component:
    """A message indicating that the maintenance request is being processed."""
    return rx.box(
        rx.box(
            rx.hstack(
                rx.icon(tag="check_circle", height="2em", width="1em", color="white"),
                rx.text("Maintenance request submitted."),
            ),
            shadow=styles.shadow_light,
            **styles.message_style,
            text_align="left",
            margin_top="1em",
            bg="#538F88",
        )
    )


def chat() -> rx.Component:
    """List all the messages in a single conversation."""
    return rx.vstack(
        rx.box(
            rx.foreach(State.chats[State.current_chat], message),
            rx.cond(State.form_processing, processing_message(), rx.box()),
            rx.cond(State.maintenance_request_submitted, submitted_message(), rx.box()),
        ),
        py="8",
        flex="1",
        width="100%",
        max_w="3xl",
        padding_x="4",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.box(
        rx.vstack(
            rx.form(
                rx.form_control(
                    rx.hstack(
                        # rx.upload(
                        #     rx.button(
                        #         rx.icon(tag="attachment"),
                        #         style=styles.upload_button,
                        #     ),
                        #     id="file_upload",
                        #     multiple=True,
                        # accept={
                        #     "application/pdf": [".pdf"],
                        #     "image/png": [".png"],
                        #     "image/jpeg": [".jpg", ".jpeg"],
                        #     "image/gif": [".gif"],
                        #     "image/webp": [".webp"],
                        #     "text/html": [".html", ".htm"],
                        # },
                        # max_files=5,
                        # disabled=False,
                        # on_keyboard=True,
                        # ),
                        rx.cond(
                            State.maintenance_request_submitted,
                            # rx.tooltip(
                            rx.input(
                                placeholder="Provide details regarding issue...",
                                id="question",
                                _placeholder={"color": "#fffa"},
                                _hover={"border_color": styles.accent_color},
                                style=styles.input_style,
                                is_disabled=True,
                            ),
                            # label="Maintenance request submitted. Create a new request.",
                            # ),
                            rx.input(
                                placeholder="Provide details regarding issue...",
                                id="question",
                                _placeholder={"color": "#fffa"},
                                _hover={"border_color": styles.accent_color},
                                style=styles.input_style,
                            ),
                        ),
                        rx.cond(
                            State.maintenance_request_submitted,
                            rx.button(
                                rx.cond(
                                    State.question_processing,
                                    loading_icon(height="1em"),
                                    rx.text("Send"),
                                ),
                                is_disabled=True,
                                type_="submit",
                                _hover={"bg": styles.accent_color},
                                style=styles.input_style,
                            ),
                            rx.button(
                                rx.cond(
                                    State.question_processing,
                                    loading_icon(height="1em"),
                                    rx.text("Send"),
                                ),
                                type_="submit",
                                _hover={"bg": styles.accent_color},
                                style=styles.input_style,
                            ),
                        ),
                    ),
                    is_disabled=State.question_processing,
                ),
                on_submit=State.process,
                reset_on_submit=True,
                width="100%",
            ),
            rx.text(
                "Disclaimer: This application is a demo and may require enhancements and proper guardrails; user discretion is advised.",
                font_size="xs",
                color="#fff6",
                text_align="center",
            ),
            width="100%",
            max_w="3xl",
            mx="auto",
        ),
        position="sticky",
        bottom="0",
        left="0",
        py="4",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {styles.border_color}",
        align_items="stretch",
        width="100%",
    )
