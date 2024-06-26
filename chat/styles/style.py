import reflex as rx

navbar: dict[str, str] = {
    "width": "100%",
    "padding": "0.75em 1em",
    "justify_content": "space-between",
    "position": "sticky",
    "top": "0",
    "bg": rx.color_mode_cond(
        "rgba(255, 255, 255, 0.81)",
        "rgba(18, 17, 19, 0.81)",
    ),
    "align_items": "center",
    "z_index": "10",
}

inner: dict[str, str] = {
    "display": "flex",
    "align_items": "center",
}
