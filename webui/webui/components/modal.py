import reflex as rx
from webui.state import State
import pandas as pd


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Add Maintenace Request"),
                            rx.icon(
                                tag="close",
                                font_size="sm",
                                on_click=State.toggle_modal,
                                color="#fff8",
                                _hover={"color": "#FFFFFF"},
                                cursor="pointer",
                            ),
                        ),
                        rx.text(
                            "Please review the the details below to ensure a prompt and effective response to your maintenance request.",
                            color="#C0C0C0",
                            font_size="sm",
                        ),
                        rx.divider(
                            border_color="#282828",
                            variant="solid",
                            orientation="horizontal",
                            border_top="3px solid #282828",
                            border_radius="1px",
                        ),
                        align_items="center",
                        justify_content="space-between",
                    )
                ),
                rx.modal_body(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.text("Tenant"),
                                rx.box(
                                    rx.hstack(
                                        rx.avatar(name="Demo User", size="sm"),
                                        rx.text("Demo User"),
                                        spacing="2",
                                    ),
                                ),
                            ),
                            # ),
                            rx.vstack(
                                rx.hstack(
                                    rx.text("Contact Email"),
                                    rx.tooltip(
                                        rx.icon(tag="info_outline"),
                                        label="If email is invalid, adjust in your profile settings.",
                                    ),
                                ),
                                rx.input(
                                    value="demo@maintenance.xyz", is_disabled=True
                                ),
                                text_align="left",
                            ),
                        ),
                        rx.divider(
                            border_color="#282828",
                            variant="solid",
                            orientation="horizontal",
                            border_top="3px solid #282828",
                            border_radius="1px",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text("Category"),
                                rx.select(
                                    ["HVAC", "Plumbing", "Electrical", "Other"],
                                    default_value="HVAC",
                                    # max_width="50%",
                                    size="sm",
                                ),
                            ),
                            rx.vstack(
                                rx.text("Urgency"),
                                rx.select(
                                    ["Low", "Normal", "High"],
                                    is_disabled=True,
                                    default_value="Normal",
                                    # max_width="50%",
                                    size="sm",
                                ),
                            ),
                            margin_top="1em",
                        ),
                        rx.vstack(
                            rx.text("Subject"),
                            rx.input(value="AC Unit Not Working"),
                        ),
                        rx.vstack(rx.text("Description"), rx.text_area()),
                    ),
                    rx.checkbox(
                        "Authorize staff to enter your property in your absence",
                        size="sm",
                        color_scheme="green",
                        # value=True,
                        margin_top="1em",
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Close",
                        # bg="#5535d4",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        margin_right="0.5em",
                        color_scheme="blackAlpha",
                        # _hover={"bg": "#4c2db3"},
                        on_click=State.toggle_modal,
                    ),
                    rx.button(
                        "Submit",
                        bg="#5535d4",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#4c2db3"},
                        on_click=State.submit_maintenance_request,
                    ),
                ),
                bg="#222",
                color="#fff",
            )
        ),
        is_open=State.modal_open,
        size="md",
    )
