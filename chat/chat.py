"""The main Chat app."""

import reflex as rx

from chat.components import chat, navbar


def index() -> rx.Component:
    """The main app."""
    return rx.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        height="100dvh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="purple",
    ),
)
app.add_page(index)
