import pynecone as pc


class WebuiConfig(pc.Config):
    pass


config = WebuiConfig(
    app_name="webui",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    frontend_packages=[
        "react-loading-icons",
    ],
)
