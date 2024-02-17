"""The main Chat app."""

import reflex as rx

from webui import styles
from webui.components import chat, modal, navbar, sidebar
from webui.state import State


def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        navbar(),
        chat.chat(),
        chat.action_bar(),
        sidebar(),
        modal(),
        bg=styles.bg_dark_color,
        color=styles.text_light_color,
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(style=styles.base_style)
app.add_page(index)
