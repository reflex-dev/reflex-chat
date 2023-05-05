import pynecone as pc


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
                    on_click=State.toggle_modal,
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
        border_bottom="1px solid #fff1",
        position="sticky",
        top="0",
        z_index="100",
    )
