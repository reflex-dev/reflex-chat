import pynecone as pc
from .styles import *


def navbar(State):
    """The navbar."""
    return pc.box(
        pc.hstack(
            pc.link(
                pc.hstack(pc.image(src="favicon.ico"), pc.heading("ChatGPT Web")),
                href="/",
            ),
            pc.menu(
                pc.menu_button(
                    pc.avatar(name="Test", size="md", bg = "black", color = "white"),
                    pc.box(),
                ),
                pc.menu_list(
                    pc.menu_item("Help"),
                    pc.link(
                        pc.menu_item("Resources"),
                        href="/",
                    ),
                    pc.menu_divider(),
                    pc.menu_item("Settings"),
                ),
            ),
            justify="space-between",
            border_bottom="0.2em solid #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bg="rgba(255,255,255, 1)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="3",
    )


def show_chat(State, chat):
    return pc.cond(
        State.current_chat == chat,
        pc.box(
        pc.text(chat),
        on_click=State.set_chat(chat),
        padding="1em",
        border_radius="5px",
        width="100%",
        border=f"0.15em solid {green_color}",
        bg=accent_color,
        shadow="lg"
    ),
    pc.box(
        pc.text(chat),
        on_click=State.set_chat(chat),
        padding="1em",
        border_radius="5px",
        width="100%",
        border="0.1em solid rgba(234,234,234, 1)",
        bg=accent_color,
    )
    )


def sidebar(State):
    return pc.flex(
        pc.vstack(
            pc.hstack(
                pc.icon(tag="add", color=text_dark_color),
                pc.text("New Chat", color=text_dark_color),
                on_click=State.change,
                padding="1em",
                border="0.1em solid rgba(234,234,234, 1)",
                border_radius="5px",
                width="100%",
            ),
            pc.foreach(State.chat_title, lambda chat: show_chat(State, chat)),
            pc.spacer(),
            pc.hstack(
                pc.box(
                    pc.icon(tag="settings", color=text_dark_color),
                    padding=".5em",
                    border="0.1em solid rgba(234,234,234, 1)",
                    border_radius="5px",
                ),
                pc.box(
                    pc.icon(tag="info_outline", color=text_dark_color),
                    padding=".5em",
                    border="0.1em solid rgba(234,234,234, 1)",
                    border_radius="5px",
                ),
                pc.spacer(),
                pc.box(
                    pc.icon(tag="external_link", color=text_dark_color),
                    padding=".5em",
                    border="0.1em solid rgba(234,234,234, 1)",
                    border_radius="5px",
                ),
                width = "100%",
            ),
            width="20em",
            padding_x="2em",
            padding_y="1em",
            padding_bottom="3em",
        ),
        pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header("Create a new chat"),
                pc.modal_body(
                    pc.vstack(
                        pc.input(
                            placeholder="Chat Name",
                            on_blur=State.set_new_chat_name,
                        ),
                        pc.select(
                            State.models,
                            on_change=State.set_current_model
                        )
                    )
                ),
                pc.modal_footer(
                    pc.hstack(
                        pc.button(
                            "Close", on_click=State.change
                        ),
                        pc.button(
                            "Create Chat", on_click=State.create_chat
                        )
                    )
                ),
            )
        ),
        is_open=State.show,
        ),
        position="fixed",
        z_index="2",
        height="100%",
        left="0px",
        top="0px",
        border_right="0.2em solid #F0F0F0",
        padding_top="6em",
        display=["none", "none", "none", "flex", "flex"]
    )
