import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    explanation_provider: str = os.getenv(
        "EXPLANATION_PROVIDER",
        "gemini"
    )

    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    max_output_tokens: int = int(
        os.getenv(
            "MAX_OUTPUT_TOKENS",
            "1200"
        )
    )


settings = Settings()