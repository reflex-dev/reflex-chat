from typing import List
import reflex as rx

options: List[str] = ["Option 1", "Option 2", "Option 3"]


class MultiSelectState(rx.State):
    option: List[str] = []


def index():
    return rx.vstack(
        rx.heading(MultiSelectState.option),
            options,
            placeholder="Select examples",
            is_multi=True,
            on_change=MultiSelectState.set_option,
            close_menu_on_select=False,
            color_schemes="twitter",
        )