import reflex as rx

from ..states.drawer import Drawer
from ..states.state import State
from ..styles.style import navbar, inner


def create_event_button(path: str, function: callable, message: str):
    def create_image(_path: str):
        return rx.image(
            src=path,
            width="21px",
            height="21px",
            filter=rx.color_mode_cond(
                "invert(0)",
                "invert(1)",
            ),
        )

    return rx.tooltip(
        rx.button(
            create_image(path),
            cursor="pointer",
            variant="ghost",
            color_scheme="gray",
            padding="0.25em",
            on_click=function,
        ),
        content=message,
    )


def big_screen_navbar():
    return rx.hstack(
        create_event_button(
            "sidebar.svg",
            Drawer.toggle_sidebar,
            "Toggle Sidebar",
        ),
        create_event_button(
            "new_chat.svg",
            Drawer.toggle_new_chat,
            "New Chat",
        ),
        # rx.color_mode.button(size="1", variant="ghost"),
        display=["none", "none", "none", "none", "flex"],
        align_items="center",
        justify_content="center",
        spacing="5",
    )


def small_screen_item(title: str, path: str):
    return rx.chakra.menu_item(
        rx.hstack(
            rx.text(title),
            rx.image(
                src=path,
                width="20px",
                height="20px",
                filter=rx.color_mode_cond(
                    "invert(0)",
                    "invert(1)",
                ),
            ),
            justify_content="space-between",
            align_items="center",
            width="100%",
        ),
        width="100%",
        color="inherit",
    )


def small_screen_navbar():
    return rx.box(
        rx.chakra.menu(
            rx.chakra.menu_button(rx.icon(tag="menu")),
            rx.chakra.menu_list(
                small_screen_item("Toggle Sidebar", "sidebar.svg"),
                small_screen_item("New Chat", "new_chat.svg"),
                font_size="var(--chakra-fontSizes-sm)",
            ),
            bg="inherit",
        ),
        display=["flex", "flex", "flex", "flex", "none"],
    )


def render_chat_navbar():
    return rx.hstack(
        # left side header ...
        rx.hstack(
            rx.box(
                rx.heading(State.title, size="3", width="250px", text_overflow="ellipsis", overflow="hidden", white_space="nowrap",),
                padding="0.6em 1.5em 0.6em 0.6em",
            ),
            **inner,
        ),
        # right side header ...
        rx.hstack(
            big_screen_navbar(),
            small_screen_navbar(),
            **inner,
            spacing="4",
        ),
        **navbar,
        background_color=rx.color("mauve", 1)
    )
