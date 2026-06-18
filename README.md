# Multimodal Moderation Trainer

Multimodal Moderation Trainer is a Python application for reviewing customer-service content before it reaches a customer-facing conversation. It combines modality-specific moderation agents for text, images, audio, and video with a simulated customer chat experience, a FastAPI backend, and Phoenix tracing for observability.

The project demonstrates how LLM-driven moderation workflows can be composed into a training environment where human-written responses are checked for policy and tone before they are delivered.

## Features

- Moderates text, image, audio, and video content with dedicated Pydantic AI agents
- Screens for PII, unfriendly or unprofessional text, disturbing media, and low-quality media
- Provides a Gradio chat interface for a trainee support agent interacting with a simulated customer
- Exposes REST endpoints through FastAPI for programmatic moderation
- Captures traces in Arize Phoenix to inspect moderation and customer-agent behavior
- Includes automated tests and evaluation scripts for the core moderation flows

## Architecture

The application is organized around a small set of services and reusable agent modules:

- `multimodal_moderation/agents/` contains the modality-specific moderation agents plus the simulated customer agent
- `multimodal_moderation/fastapi_app.py` exposes HTTP endpoints for moderation
- `multimodal_moderation/gradio_app.py` provides the interactive training UI
- `multimodal_moderation/app.py` launches Phoenix, the API server, and the chat UI together
- `multimodal_moderation/tracing.py` configures observability for Phoenix
- `evals/` contains lightweight evaluation scripts and sample test cases
- `tests/` covers environment loading, moderation result schemas, and app behavior

## Technology Stack

- Python 3.12
- FastAPI and Uvicorn
- Gradio
- Pydantic AI
- Google Gemini models through `google-genai`
- Arize Phoenix / OpenInference tracing
- Pytest

## Setup

### 1. Create an environment and install dependencies

Using `uv`:

```bash
uv sync --dev
uv pip install -e .
```

Using `pip` and `venv`:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Configure environment variables

Copy `env.example` to `.env` and provide values for the required settings:

```bash
cp env.example .env
```

Required variables:

- `USER_API_KEY`: shared key used by the Gradio client when calling the FastAPI API
- `GEMINI_API_KEY`: API key for Google Gemini
- `DEFAULT_GOOGLE_MODEL`: default model name used by the moderation and customer agents

Optional variables:

- `API_BASE_URL`: defaults to `http://localhost:8000`
- `PHOENIX_URL`: defaults to `http://127.0.0.1:6006`
- `GOOGLE_GEMINI_BASE_URL`: optional override for custom Gemini-compatible endpoints
- `EVAL_JUDGE_MODEL` and `EVAL_NUM_REPEATS`: evaluation settings

## Running the Application

### Launch the full local experience

```bash
uv run multimodal-moderation
```

This starts:

- Phoenix at `http://localhost:6006`
- FastAPI at `http://localhost:8000`
- Gradio at `http://localhost:7860`

### Run only the API

```bash
uv run multimodal-moderation-api
```

### Run only the chat interface

```bash
uv run multimodal-moderation-chat
```

## API Endpoints

Once the API is running, the main routes are:

- `POST /api/v1/moderate_text`
- `POST /api/v1/moderate_image_file`
- `POST /api/v1/moderate_video_file`
- `POST /api/v1/moderate_audio_file`
- `GET /api/v1/health`

Interactive API docs are available at `http://localhost:8000/docs`.

## Testing

Run the automated test suite:

```bash
pytest
```

The default test run excludes live integration tests that require a working Gemini key and outbound network access.

Or with `uv`:

```bash
uv run pytest tests/ -vv
```

To run the live integration test intentionally:

```bash
pytest -m integration
```

The repository also includes evaluation scripts:

```bash
uv run evals/text/test_cases.py
uv run evals/image/test_cases.py
uv run evals/audio/test_cases.py
uv run evals/video/test_cases.py
```

## Design Decisions and Tradeoffs

- Separate moderation agents by modality: text, image, audio, and video each have different failure modes and review criteria, so the project keeps their prompts and schemas isolated instead of forcing one generic moderation prompt.
- FastAPI plus Gradio split: the API and the UI are intentionally separate so the moderation service can support other frontends without rewriting the moderation logic.
- LLM-mediated moderation: this enables flexible reasoning across modalities, but it also means outputs can vary by model choice and prompt behavior.
- Static API key authentication: the included auth mechanism is intentionally lightweight for local development and demonstration. It is not appropriate for production use.
- External-model dependency: real moderation quality depends on Gemini availability, configuration, and model behavior. Local tests cover application behavior, but full end-to-end moderation quality still depends on live model access.

## Limitations

- The project depends on external Gemini access for real moderation and customer-agent responses.
- Media moderation thresholds are prompt-driven rather than based on deterministic classifiers.
- The included authentication flow is for local/demo scenarios only.
- Evaluation coverage is helpful for smoke testing but does not replace production benchmarking or safety review.

## Repository Notes

- Sample media used by tests and evaluations is intentionally checked in.
- Generated caches, local virtual environments, `.env`, and packaging artifacts should not be committed.

## Future Improvements

- Add moderation categories for spam, hate speech, or misinformation
- Add a dashboard view that summarizes flagged content trends
- Expand the simulated customer into multiple personas and escalation styles

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
