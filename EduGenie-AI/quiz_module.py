import json

from ai_client import generate_json


QUIZ_SCHEMA = {

    "type": "object",

    "properties": {

        "questions": {

            "type": "array",

            "minItems": 3,

            "maxItems": 3,

            "items": {

                "type": "object",

                "properties": {

                    "question": {
                        "type": "string"
                    },

                    "options": {

                        "type": "array",

                        "minItems": 4,

                        "maxItems": 4,

                        "items": {
                            "type": "string"
                        }
                    },

                    "correct_answer": {
                        "type": "string"
                    },

                    "explanation": {
                        "type": "string"
                    }
                },

                "required": [
                    "question",
                    "options",
                    "correct_answer",
                    "explanation"
                ]
            }
        }
    },

    "required": [
        "questions"
    ]
}


async def generate_quiz(
    text: str
) -> dict:

    prompt = f"""
Create exactly THREE multiple-choice questions
from the educational passage below.

Rules:

1. Create exactly 3 questions.
2. Each question must have exactly 4 options.
3. Only one option can be correct.
4. correct_answer must exactly match
   one of the four option strings.
5. Provide a short explanation.
6. Questions must be answerable using
   the supplied passage.
7. Do not create trick questions.
8. Do not introduce unrelated information.

Passage:

{text}
"""

    raw = await generate_json(
        prompt,
        QUIZ_SCHEMA
    )

    data = json.loads(
        raw
    )

    questions = data.get(
        "questions",
        []
    )

    if len(questions) != 3:

        raise ValueError(
            "The AI did not return exactly "
            "three questions."
        )

    for question in questions:

        options = question.get(
            "options",
            []
        )

        if len(options) != 4:

            raise ValueError(
                "Every quiz question must "
                "contain exactly four options."
            )

        if (
            question["correct_answer"]
            not in options
        ):

            raise ValueError(
                "The correct answer does not "
                "match any provided option."
            )

    return data