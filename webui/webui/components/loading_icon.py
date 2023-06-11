import pynecone as pc


class LoadingIcon(pc.Component):
    """A custom loading icon component."""

    library = "react-loading-icons"
    tag = "SpinningCircles"
    stroke: pc.Var[str]
    stroke_opacity: pc.Var[str]
    fill: pc.Var[str]
    fill_opacity: pc.Var[str]
    stroke_width: pc.Var[str]
    speed: pc.Var[str]
    height: pc.Var[str]

    @classmethod
    def get_controlled_triggers(cls) -> dict[str, pc.Var]:
        return {"on_change": pc.EVENT_ARG}


loading_icon = LoadingIcon.create
