import reflex as rx
from chat.state import State


def provider_selector() -> rx.Component:
    """Create a provider selection component."""
    return rx.card(
        rx.vstack(
            rx.heading("LLM Provider Settings", size="4", weight="bold"),
            rx.text(
                "Choose your LLM provider and model",
                size="2",
                color=rx.color("mauve", 10),
            ),
            # Provider Selection
            rx.hstack(
                rx.text("Provider:", weight="medium"),
                rx.select(
                    State.available_providers,
                    placeholder="Select provider",
                    value=State.current_provider,
                    on_change=State.set_provider,
                    width="200px",
                ),
                rx.spinner(
                    size="2",
                    loading=State.processing,
                ),
                align="center",
                spacing="3",
            ),
            # Model Selection
            rx.hstack(
                rx.text("Model:", weight="medium"),
                rx.select(
                    State.available_models,
                    placeholder="Select model",
                    value=State.current_model,
                    on_change=State.set_model,
                    width="250px",
                ),
                rx.cond(
                    State.available_models.length() == 0,
                    rx.tooltip(
                        rx.icon("info", size=16),
                        content="No models available. Check your provider configuration.",
                    ),
                ),
                align="center",
                spacing="3",
            ),
            # Error Display
            rx.cond(
                State.provider_error != "",
                rx.callout(
                    rx.icon("triangle_alert", size=4),
                    rx.text(State.provider_error),
                    color_scheme="red",
                    variant="soft",
                ),
            ),
            # Status Indicator
            rx.hstack(
                rx.cond(
                    State._provider_instance != None,
                    rx.hstack(
                        rx.icon("check-circle", size=4, color=rx.color("green", 10)),
                        rx.text(
                            "Provider ready", size="2", color=rx.color("green", 10)
                        ),
                    ),
                    rx.hstack(
                        rx.icon("x-circle", size=4, color=rx.color("red", 10)),
                        rx.text(
                            "Provider not configured",
                            size="2",
                            color=rx.color("red", 10),
                        ),
                    ),
                ),
                rx.spacer(),
                rx.button(
                    "Refresh Models",
                    size="2",
                    variant="outline",
                    on_click=State.update_available_models,
                    loading=State.processing,
                ),
                align="center",
                width="100%",
            ),
            # Configuration Help
            rx.divider(),
            rx.accordion.root(
                rx.accordion.item(
                    header="Configuration Help",
                    content=rx.vstack(
                        rx.text("Environment variables needed:", weight="medium"),
                        rx.code_block(
                            """# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5-mini

# Ollama (local models)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma3:4b

# Google Gemini
GEMINI_API_KEY=your_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.0-flash

# Provider Selection
LLM_PROVIDER=openai  # or ollama, gemini
""",
                            language="bash",
                            width="100%",
                        ),
                        rx.text(
                            "Note: Models are dynamically fetched when possible. If no models appear, ensure your MODEL environment variable is set.",
                            size="1",
                        ),
                        align="start",
                        spacing="2",
                    ),
                    value="config-help",
                ),
                collapsible=True,
                width="100%",
            ),
            spacing="4",
            align="stretch",
            width="100%",
        ),
        padding="20px",
        radius="12px",
        background_color=rx.color("mauve", 1),
        border=f"1px solid {rx.color('mauve', 3)}",
        width="100%",
        max_width="600px",
    )


def provider_status_bar() -> rx.Component:
    """Create a compact provider status bar for the navbar."""
    return rx.hstack(
        rx.icon("bot", size=4, color=rx.color("accent", 10)),
        rx.text(
            f"{State.current_provider}: {State.current_model}",
            size="2",
            weight="medium",
            color=rx.color("mauve", 11),
        ),
        rx.cond(
            State.provider_error != "",
            rx.tooltip(
                rx.icon("triangle_alert", size=3, color=rx.color("red", 10)),
                content=State.provider_error,
            ),
        ),
        rx.cond(
            State.processing,
            rx.spinner(size="2", color=rx.color("accent", 10)),
        ),
        align="center",
        spacing="2",
        padding_x="12px",
        padding_y="6px",
        radius="8px",
        background_color=rx.color("mauve", 2),
        border=f"1px solid {rx.color('mauve', 4)}",
    )
