import pynecone as pc

from webui import styles
from webui.state import State


def navbar():
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
                    bg=styles.accent_color,
                    px="4",
                    py="2",
                    h="auto",
                    on_click=State.toggle_modal,
                ),
                pc.menu(
                    pc.menu_button(
                        pc.avatar(name="User", size="md"),
                        pc.box(),
                    ),
                    pc.menu_list(
                        pc.menu_item("Help"),
                        pc.menu_divider(),
                        pc.menu_item("Settings"),
                    ),
                ),
                spacing="8",
            ),
            justify="space-between",
        ),
        bg=styles.bg_dark_color,
        backdrop_filter="auto",
        backdrop_blur="lg",
        p="4",
        border_bottom=f"1px solid {styles.border_color}",
        position="sticky",
        top="0",
        z_index="100",
    )
