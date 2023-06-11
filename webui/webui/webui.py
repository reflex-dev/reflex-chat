"""The main Chat app."""

import pynecone as pc

from webui import styles
from webui.components import chat, modal, navbar, sidebar
from webui.state import State


def index() -> pc.Component:
    """The main app."""
    return pc.vstack(
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
app = pc.App(state=State, style=styles.base_style)
app.add_page(index)
app.compile()
