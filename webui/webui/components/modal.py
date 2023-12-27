import reflex as rx
from webui.state import State
import pandas as pd

# TODO
sample_df = pd.DataFrame(
    [
        {
            "Subject": "AC Unit Not Working",
            "Description": "The AC unit in the apartment is not turning on. The power supply and circuit breaker have been checked and do not appear to be the cause of the problem.",
            "CategoryId": "HVAC",
            "TaskPriority": "High",
        }
    ]
)


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Maintenace Request"),
                        rx.icon(
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
                rx.modal_body(
                    rx.data_table(
                        data=sample_df[
                            ["Subject", "Description", "CategoryId", "TaskPriority"]
                        ],
                        pagination=True,
                        bg="#222",
                        border_color="#fff3",
                        _placeholder={"color": "#fffa"},
                    ),
                    # rx.input(
                    #     placeholder="Provide details regarding issue...",
                    #     on_blur=State.set_new_chat_name,
                    #     bg="#222",
                    #     border_color="#fff3",
                    #     _placeholder={"color": "#fffa"},
                    # ),
                ),
                rx.modal_footer(
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
            ),
        ),
        is_open=State.modal_open,
        size="md",
    )


def modal() -> rx.Component:
    """A modal to create a new chat."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.hstack(
                        rx.text("Maintenace Request"),
                        rx.icon(
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
                rx.modal_body(
                    rx.stack(
                        rx.skeleton(height="10px", speed=1.5),
                        rx.skeleton(height="15px", speed=1.5),
                        rx.skeleton(height="20px", speed=1.5),
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Submit",
                        is_disabled=True,
                        bg="#5535d4",
                        box_shadow="md",
                        px="4",
                        py="2",
                        h="auto",
                        _hover={"bg": "#4c2db3"},
                        on_click=State.submit_maintenance_request,
                    ),
                    bg="#222",
                    color="#fff",
                ),
            )
        ),
        is_open=State.modal_open,
        size="md",
    )