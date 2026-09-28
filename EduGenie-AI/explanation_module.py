from functools import lru_cache

from config import settings
from ai_client import generate_text


@lru_cache(maxsize=1)
def get_local_pipeline():
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        tokenizer=settings.local_explanation_model,
    )


def local_explain(topic: str) -> str:
    generator = get_local_pipeline()

    prompt = (
        "Explain the following topic to a beginner "
        "using simple and concise language. "
        "Use one example if helpful. "
        "Topic: "
        + topic
    )

    result = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False,
    )

    return result[0]["generated_text"].strip()


async def explain_topic(topic: str) -> str:
    if settings.explanation_provider.lower() == "local":
        try:
            return local_explain(topic)

        except Exception as exc:
            fallback = await gemini_explain(topic)

            return (
                fallback
                + "\n\n"
                "[Note: Local LaMini explanation "
                "was unavailable, so Gemini fallback "
                f"was used: {type(exc).__name__}]"
            )

    return await gemini_explain(topic)


async def gemini_explain(topic: str) -> str:
    prompt = f"""
Explain the topic below as a patient
educational tutor.

Topic:

{topic}

Assume the learner may have no prior
knowledge.

Structure your explanation as:

1. What it is
2. How it works
3. A simple example or analogy
4. One key takeaway

Use clear language and avoid unnecessary jargon.
"""

    return await generate_text(prompt)