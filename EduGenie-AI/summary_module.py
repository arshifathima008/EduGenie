from ai_client import generate_text


async def summarize_text(
    text: str
) -> str:

    prompt = f"""
You are EduGenie, an educational AI tutor.

Summarize the educational passage below.

Rules:

1. Preserve the main ideas and important facts.
2. Use simple language suitable for students.
3. Keep the summary concise.
4. Do not introduce information that is not present
   in the passage.
5. Do not invent citations or sources.
6. Use short paragraphs or bullet points when helpful.

Educational passage:

{text}
"""

    return await generate_text(prompt)