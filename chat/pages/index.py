import reflex as rx

from ..components.chat import chat, action_bar
from ..components.navbar import render_chat_navbar
from ..components.drawers import render_new_chat_dialog, render_rename_dialog
from ..components.sidebar import render_drawer


@rx.page("/")
def index() -> rx.Component:
    """The main app."""
    return rx.vstack(
        render_drawer(),
        render_new_chat_dialog(),
        render_rename_dialog(),
        render_chat_navbar(),
        chat(),
        action_bar(),
        background_color=rx.color("mauve", 1),
        color=rx.color("mauve", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
        width="100%",
    )
