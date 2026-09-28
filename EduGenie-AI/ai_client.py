from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


class GeminiConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )
    return genai.Client(api_key=settings.gemini_api_key)


async def generate_text(prompt: str, temperature: float = 0.3) -> str:
    """Generate text using Gemini. Note: temperature/max_output_tokens
    are ignored because Gemini 3.8 Flash does not accept them."""
    client = get_client()

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


async def generate_json(prompt: str, schema: dict) -> str:
    """Generate structured JSON using Gemini."""
    client = get_client()

    response = await client.aio.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return text