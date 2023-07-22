import reflex as rx


class LoadingIcon(rx.Component):
    """A custom loading icon component."""

    library = "react-loading-icons"
    tag = "SpinningCircles"
    stroke: rx.Var[str]
    stroke_opacity: rx.Var[str]
    fill: rx.Var[str]
    fill_opacity: rx.Var[str]
    stroke_width: rx.Var[str]
    speed: rx.Var[str]
    height: rx.Var[str]

    @classmethod
    def get_controlled_triggers(cls) -> dict[str, rx.Var]:
        return {"on_change": rx.EVENT_ARG}


loading_icon = LoadingIcon.create
