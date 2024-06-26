import reflex as rx

from ..states.state import State
from ..states.drawer import Drawer, SidebarOption


def create_sidebar_menu_item(name: str, tag: str, color: str, function: callable):
    return rx.hstack(
        rx.text(name),
        rx.icon(tag=tag, size=14),
        color=color,
        width="100%",
        justify_content="space-between",
        align_items="center",
        on_click=function,
    )


def sidebar_item_option_menu(data: str):
    return rx.menu.root(
        rx.menu.trigger(
            rx.icon(tag="ellipsis", size=16, cursor="pointer"),
        ),
        rx.menu.content(
            rx.menu.item(
                create_sidebar_menu_item(
                    "Rename",
                    "file-pen",
                    "inherit",
                    Drawer.toggle_rename(data),
                )
            ),
            rx.menu.item(
                create_sidebar_menu_item(
                    "Delete",
                    "trash-2",
                    "red",
                    SidebarOption.delete_chat(data),
                )
            ),
        ),
    )


def sidebar_item(data: str):
    return rx.button(
        rx.hstack(
            rx.text(
                data + " ",
                white_space="nowrap",
                text_overflow="ellipsis",
                width="199px",
                text_align="start",
                overflow="hidden",
                weight="medium",
            ),
            sidebar_item_option_menu(data),
            width="100%",
            justify_content="space-between",
            align_items="center",
            display="flex",
        ),
        width="100%",
        variant="ghost",
        cursor="pointer",
        color="inherit",
        color_scheme="gray",
        on_click=Drawer.select_chat(data),
    )


def render_drawer():
    return rx.drawer.root(
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.box(
                        rx.heading(
                            "Chat History",
                            size="3",
                        ),
                        padding="1.35em 1.25em 0.6em 1.25em",
                        align_items="center",
                    ),
                    rx.vstack(
                        rx.foreach(State.chat_titles, sidebar_item),
                        width="100%",
                        padding="1.25em",
                    ),
                    background_color=rx.color("mauve", 3),
                    width="100%",
                    height="100%",
                ),
                on_interact_outside=Drawer.toggle_sidebar(),
                height="100%",
                width="20em",
                top="auto",
                right="auto",
            ),
        ),
        direction="left",
        open=Drawer.is_sidebar_open,
    )
