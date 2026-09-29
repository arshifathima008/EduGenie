import asyncio
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


async def _call_with_retry(func, max_retries=4):
    """Retry on 503 UNAVAILABLE errors with exponential backoff."""
    last_error = None
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 3 * (attempt + 1)  # 3s, 6s, 9s
                    await asyncio.sleep(wait_time)
                    continue
            raise
    raise last_error


async def generate_text(prompt: str, temperature: float = 0.3) -> str:
    client = get_client()

    async def _call():
        return await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )

    response = await _call_with_retry(_call)

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


async def generate_json(prompt: str, schema: dict) -> str:
    client = get_client()

    async def _call():
        return await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

    response = await _call_with_retry(_call)

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty JSON response.")
    return text