import pynecone as pc

from .styles import *


def navbar(State):
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.icon(
                    tag="hamburger",
                    mr=4,
                    on_click=State.toggle_drawer,
                    cursor="pointer",
                ),
                pc.link(
                    pc.box(
                        pc.image(src="favicon.ico", width=30, height="auto"),
                        p="1",
                        border_radius="6",
                        bg="#F0F0F0",
                        mr="2",
                    ),
                    href="/",
                ),
                pc.breadcrumb(
                    pc.breadcrumb_item(
                        pc.heading("PyneconeGPT", size="sm"),
                    ),
                    pc.breadcrumb_item(
                        pc.text(State.current_chat, size="sm", font_weight="normal"),
                    ),
                ),
            ),
            pc.hstack(
                pc.button(
                    "+ New chat",
                    bg="#5535d4",
                    box_shadow="md",
                    px="4",
                    py="2",
                    h="auto",
                    _hover={"bg": "#4c2db3"},
                ),
                pc.menu(
                    pc.menu_button(
                        pc.avatar(name="User", size="sm", bg="#333", color="white"),
                        pc.box(),
                    ),
                    pc.menu_list(
                        pc.menu_item(
                            "Help", _hover={"bg": "#fff3"}, _focus={"bg": "#fff3"}
                        ),
                        pc.menu_divider(border_color="#fff3"),
                        pc.menu_item(
                            "Settings", _hover={"bg": "#fff3"}, _focus={"bg": "#fff3"}
                        ),
                        bg="#111",
                        border_color="#fff3",
                    ),
                ),
                spacing="8",
            ),
            justify="space-between",
        ),
        bg="#1114",
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        border_bottom="1px solid #fff3",
        position="sticky",
        top="0",
        z_index="100",
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
            shadow="lg",
        ),
        pc.box(
            pc.text(chat),
            on_click=State.set_chat(chat),
            padding="1em",
            border_radius="5px",
            width="100%",
            border="0.1em solid rgba(234,234,234, 1)",
            bg=accent_color,
        ),
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
                ),
            ),
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
                            pc.select(State.models, on_change=State.set_current_model),
                        )
                    ),
                    pc.modal_footer(
                        pc.hstack(
                            pc.button("Close", on_click=State.change),
                            pc.button("Create Chat", on_click=State.create_chat),
                        )
                    ),
                )
            ),
            is_open=State.show,
        ),
    )
