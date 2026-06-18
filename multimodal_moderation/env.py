import os
from dotenv import load_dotenv
from google.genai import Client
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from multimodal_moderation.types.model_choice import ModelChoice


load_dotenv()


def _get_required_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"{key} environment variable is required but not set")
    return value


GEMINI_API_KEY: str = _get_required_env("GEMINI_API_KEY")
USER_API_KEY: str = _get_required_env("USER_API_KEY")
DEFAULT_GOOGLE_MODEL: str = _get_required_env("DEFAULT_GOOGLE_MODEL")
GOOGLE_GEMINI_BASE_URL: str | None = os.getenv("GOOGLE_GEMINI_BASE_URL")

EVAL_JUDGE_MODEL: str = os.getenv("EVAL_JUDGE_MODEL", DEFAULT_GOOGLE_MODEL)
EVAL_NUM_REPEATS: int = int(os.getenv("EVAL_NUM_REPEATS", "1"))
API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
PHOENIX_URL: str = os.getenv("PHOENIX_URL", "http://127.0.0.1:6006")


def get_google_provider() -> GoogleProvider:
    if GOOGLE_GEMINI_BASE_URL:
        return GoogleProvider(
            client=Client(
                api_key=GEMINI_API_KEY,
                http_options={"base_url": GOOGLE_GEMINI_BASE_URL},
            )
        )

    return GoogleProvider(api_key=GEMINI_API_KEY)


def get_default_model_choice() -> ModelChoice:
    return ModelChoice(
        model=GoogleModel(
            DEFAULT_GOOGLE_MODEL,
            provider=get_google_provider(),
        ),
        model_settings=GoogleModelSettings(google_thinking_config={"thinking_budget": 0}),
    )
