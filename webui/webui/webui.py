"""The main Chat app."""

import os
import reflex as rx
from webui.components import chat, navbar
from webui.state import State
from webui.layout import auth_layout


def login() -> rx.Component:
    return auth_layout(
        rx.box(
            rx.vstack(
                rx.input(
                    type="password",
                    placeholder="Password",
                    on_blur=State.set_password,
                    size="3",
                ),
                rx.button(
                    "Log in", on_click=State.check_password, size="3",
                ),
                align="center",
                spacing="4",
            ),
            background=rx.color("mauve", 1),
            border="1px solid #eaeaea",
            padding="16px",
            width="400px",
            border_radius="8px",
        ),
    )


def chatapp() -> rx.Component:
    return rx.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


def index() -> rx.Component:
    """The main app."""
    if not os.getenv("PASSWORD"):
        return chatapp()

    else:
        return rx.cond(State.correct_password, chatapp(), login())


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="red",
    ),
)
app.add_page(index)
