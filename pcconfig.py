import pynecone as pc


class LlmwebuiConfig(pc.Config):
    pass


config = LlmwebuiConfig(
    app_name="llm_web_ui",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    frontend_packages=[
        "react-loading-icons",
    ],
)
