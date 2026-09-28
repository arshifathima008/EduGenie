import json
from ai_client import generate_json


LEARNING_SCHEMA = {
    "type": "object",
    "properties": {
        "overview": {"type": "string"},
        "weeks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "week": {"type": "integer"},
                    "focus": {"type": "string"},
                    "topics": {"type": "array", "items": {"type": "string"}},
                    "practice": {"type": "string"},
                    "resources": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["week", "focus", "topics", "practice", "resources"]
            }
        },
        "final_assessment": {"type": "string"},
        "tips": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["overview", "weeks", "final_assessment", "tips"]
}


async def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 6
) -> dict:
    prompt = f"""
Create a practical learning path.

Topic: {topic}
Learner level: {level}
Duration: {weeks} weeks

The learning path should progress from the learner's current
level toward advanced understanding where appropriate.

For each week provide:
- Week number
- Main focus
- Topics
- Practice task
- Suggested resource types

Also provide:
- Overall overview
- Final assessment or mini-project
- Study tips

Important: Do not fabricate specific URLs. Return structured JSON.
"""

    raw = await generate_json(prompt, LEARNING_SCHEMA)
    return json.loads(raw)