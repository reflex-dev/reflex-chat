import reflex as rx

from ..states.state import State
from ..states.drawer import Drawer, SidebarOption


def create_dialog(
    components: list[rx.components], all_clickable: callable, is_open: bool
):
    return rx.dialog.root(
        rx.drawer.overlay(z_index="5"),
        rx.dialog.content(
            rx.hstack(
                *components,
                background_color=rx.color("mauve", 1),
                width="100%",
            ),
            width="100%",
            border_radius="6px",
            on_interact_outside=all_clickable,
        ),
        open=is_open,
    )


def render_new_chat_dialog():
    return create_dialog(
        [
            rx.input(
                placeholder="Enter chat name ...",
                on_blur=State.set_new_chat_name,
                width="100%",
            ),
            rx.dialog.close(
                rx.button(
                    "Create",
                    on_click=Drawer.create_new_chat,
                ),
            ),
        ],
        Drawer.toggle_new_chat(),
        Drawer.is_new_chat_open,
    )


def render_rename_dialog():
    return create_dialog(
        [
            rx.input(
                value=State.new_title,
                on_change=lambda e: Drawer.update_renaming_chat_input(e),
                width="100%",
            ),
            rx.dialog.close(
                rx.button(
                    "Rename",
                    on_click=SidebarOption.rename_chat,
                ),
            ),
        ],
        Drawer.toggle_rename(),
        SidebarOption.is_rename_chat_open,
    )
