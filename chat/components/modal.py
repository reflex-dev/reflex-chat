import reflex as rx
import reflex_chakra as rc

from chat.state import State


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rc.modal(
        rc.modal_overlay(
            rc.modal_content(
                rc.modal_header(
                    rc.hstack(
                        rc.text("Create new chat"),
                        rc.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_modal,
                            color="#fff8",
                            _hover={"color": "#fff"},
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                rc.modal_body(
                    rc.input(
                        placeholder="Type something...",
                        on_blur=State.set_new_chat_name,
                        bg="#222",
                        border_color="#fff3",
                        _placeholder={"color": "#fffa"},
                    ),
                ),
                rc.modal_footer(
                    rc.button(
                        "Create",
                        bg="#5535d4",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#4c2db3"},
                        on_click=State.create_chat,
                    ),
                ),
                bg="#222",
                color="#fff",
            ),
        ),
        is_open=State.modal_open,
    )
