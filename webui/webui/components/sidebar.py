import pynecone as pc

from webui import styles
from webui.state import State


def sidebar_chat(chat: str) -> pc.Component:
    """A sidebar chat item.

    Args:
        chat: The chat item.
    """
    return pc.hstack(
        pc.box(
            chat,
            on_click=lambda: State.set_chat(chat),
            style=styles.sidebar_style,
            color=styles.icon_color,
            flex="1",
        ),
        pc.box(
            pc.icon(
                tag="delete",
                style=styles.icon_style,
                on_click=State.delete_chat,
            ),
            style=styles.sidebar_style,
        ),
        color=styles.text_light_color,
        cursor="pointer",
    )


def sidebar() -> pc.Component:
    """The sidebar component."""
    return pc.drawer(
        pc.drawer_overlay(
            pc.drawer_content(
                pc.drawer_header(
                    pc.hstack(
                        pc.text("Chats"),
                        pc.icon(
                            tag="close",
                            on_click=State.toggle_drawer,
                            style=styles.icon_style,
                        ),
                    )
                ),
                pc.drawer_body(
                    pc.vstack(
                        pc.foreach(State.chat_titles, lambda chat: sidebar_chat(chat)),
                        align_items="stretch",
                    )
                ),
            ),
        ),
        placement="left",
        is_open=State.drawer_open,
    )
