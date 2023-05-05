import pynecone as pc
from webui.components import loading_icon, modal, navbar
from webui.state import State


def message(qa):
    message_style = dict(
        display="inline-block",
        p="4",
        border_radius="xl",
    )
    return pc.box(
        pc.box(
            pc.text(
                qa["question"],
                bg="#fff3",
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
        ),
        pc.box(
            pc.text(
                qa["answer"],
                bg="#5535d4",
                **message_style,
            ),
            text_align="left",
        ),
        width="100%",
    )


def chat(State):
    return pc.vstack(
        pc.box(pc.foreach(State.chats[State.current_chat], message)),
        py="8",
        align_items="stretch",
        class_name="hello",
        justify_content="space-between",
        flex="1",
        width="100%",
        max_w="3xl",
        align_self="center",
        overflow="hidden",
    )


def action_bar(State):
    return pc.box(
        pc.vstack(
            pc.hstack(
                pc.input(
                    placeholder="Type something...",
                    on_blur=State.set_question,
                    bg="#222",
                    border_color="#fff3",
                    _placeholder={"color": "#fffa"},
                ),
                pc.button(
                    pc.cond(
                        State.processing, loading_icon(height="1em"), pc.text("Send")
                    ),
                    on_click=[State.toggle_processing, State.process_question],
                    bg="#222",
                    color="#fff",
                    p="4",
                    _hover={"bg": "#5535d4", "color": "#fff"},
                ),
            ),
            pc.text(
                "PyneconeGPT may return factually incorrect or misleading responses. Use discretion.",
                font_size="xs",
                color="#fff6",
                text_align="center",
            ),
            width="100%",
            max_w="3xl",
            mx="auto",
            align_items="stretch",
        ),
        position="sticky",
        bottom="0",
        left="0",
        py="4",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top="1px solid #fff1",
        align_items="stretch",
        width="100%",
        bg="#1113",
    )


def navigate_chat(State, chat):
    return pc.hstack(
        pc.box(
            chat,
            on_click=[State.set_chat(chat), State.toggle_drawer],
            p="4",
            border="1px solid #fff3",
            border_radius="lg",
            flex="1",
        ),
        pc.icon(
            tag="delete",
            font_size="sm",
            color="#fff8",
            w="8",
            on_click=[State.delete_chat, State.toggle_drawer],
        ),
        bg="#222",
        color="#fff",
        align_items="center",
        justify_content="space-between",
        cursor="pointer",
    )


def drawer(State):
    return pc.drawer(
        pc.drawer_overlay(
            pc.drawer_content(
                pc.drawer_header(
                    pc.hstack(
                        pc.text("Chats"),
                        pc.icon(
                            tag="close",
                            font_size="sm",
                            on_click=State.toggle_drawer,
                            color="#fff8",
                            _hover={"color": "#fff"},
                            cursor="pointer",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                pc.drawer_body(
                    pc.vstack(
                        pc.foreach(
                            State.chat_title, lambda chat: navigate_chat(State, chat)
                        ),
                        align_items="stretch",
                    )
                ),
                bg="#222",
                color="#fff",
            ),
        ),
        placement="left",
        is_open=State.drawer_open,
    )


def index() -> pc.Component:
    return pc.vstack(
        navbar(State),
        chat(State),
        action_bar(State),
        drawer(State),
        modal(State),
        bg="#111",
        color="#fff",
        min_h="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
