# Reflex Chat App

A user-friendly, highly customizable Python web app designed to demonstrate LLMs in a ChatGPT format with support for multiple LLM providers.

<div align="center">
<img src="./docs/demo.gif" alt="icon"/>
</div>

# Getting Started

## Choose Your LLM Provider

The app supports three LLM providers. Configure the one you want to use:

### Option 1: OpenAI

You'll need a valid OpenAI subscription. Set your API key and model:

```bash
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
export LLM_PROVIDER="openai"
export OPENAI_MODEL="gpt-5-mini"
```

### Option 2: Ollama (Local Models)

Run models locally using Ollama:

1. [Install Ollama](https://ollama.ai/download)
2. Start Ollama server: `ollama serve`
3. Pull a model: `ollama pull gemma3:4b`
4. Configure environment:

```bash
export LLM_PROVIDER="ollama"
export OLLAMA_HOST="http://localhost:11434"  # optional, default
export OLLAMA_MODEL="gemma3:4b"  # required: must be a model you have installed
```

### Option 3: Google Gemini

Use Google's Gemini models:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
export LLM_PROVIDER="gemini"
export GEMINI_MODEL="gemini-2.0-flash"
```

For Vertex AI:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
export GOOGLE_USE_VERTEXAI="true"
export GOOGLE_PROJECT_ID="your-gcp-project-id"
export GOOGLE_LOCATION="us-central1"  # optional
```

### 🧬 1. Clone the Repo

```bash
git clone https://github.com/reflex-dev/reflex-chat.git
cd reflex-chat
```

### 📦 2. Install Dependencies

To get started with Reflex, you'll need:

- Python 3.10+
- pip dependencies: `reflex`, `openai`, `ollama`, `google-genai`

Install all dependencies with the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 🚀 3. Run the application

Initialize and run the app:

```bash
reflex init
reflex run
```

#### Model Specification:

- **OpenAI**: `OPENAI_MODEL` (your chosen model, e.g., gpt-5-mini, gpt-4o, etc.)
- **Ollama**: `OLLAMA_MODEL` (your local model, e.g., gemma3:4b, llama3.2, etc.)
  - Note: Ollama requests use `num_ctx=4096` by default for optimal context window
- **Google**: `GEMINI_MODEL` (your chosen model, e.g., gemini-2.0-flash, gemini-2.5-pro, etc.)

## Environment Variables Reference

| Variable              | Required      | Default                  | Description                          |
| --------------------- | ------------- | ------------------------ | ------------------------------------ |
| `LLM_PROVIDER`        | No            | `openai`                 | Choose: `openai`, `ollama`, `gemini` |
| `OPENAI_API_KEY`      | For OpenAI    | -                        | Your OpenAI API key                  |
| `OPENAI_MODEL`        | For OpenAI    | -                        | OpenAI model to use                  |
| `OLLAMA_HOST`         | No            | `http://localhost:11434` | Ollama server URL                    |
| `OLLAMA_MODEL`        | For Ollama    | -                        | Ollama model to use                  |
| `GEMINI_API_KEY`      | For Gemini    | -                        | Your Google API key                  |
| `GEMINI_MODEL`        | For Gemini    | -                        | Gemini Model to use                  |
| `GOOGLE_USE_VERTEXAI` | No            | `false`                  | Use Vertex AI instead                |
| `GOOGLE_PROJECT_ID`   | For Vertex AI | -                        | GCP project ID                       |
| `GOOGLE_LOCATION`     | No            | `us-central1`            | GCP region                           |

# Features

- 100% Python-based, including the UI, using Reflex
- Create and delete chat sessions
- The application is fully customizable and no knowledge of web dev is required to use it.
  - See https://reflex.dev/docs/styling/overview for more details
- Easily swap out any LLM
- Responsive design for various devices

# Contributing

We welcome contributions to improve and extend the LLM Web UI.
If you'd like to contribute, please do the following:

- Fork the repository and make your changes.
- Once you're ready, submit a pull request for review.

# License

The following repo is licensed under the MIT License.
