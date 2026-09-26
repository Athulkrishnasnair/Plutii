import json
import os

from google import genai
from google.genai import types


def create_implementation_plan(content):
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are ArrowLens Plan Lens.

Turn the developer's rough note into a practical implementation plan.

IMPORTANT RULES:
- Base the plan only on the information provided.
- Do not invent requirements that are not reasonably implied.
- Do not write a huge tutorial.
- Break the work into logical implementation steps.
- Steps should be actionable for a developer.
- Mention dependencies only when they matter.
- Include concrete verification steps.
- If the note is vague, make reasonable minimal assumptions rather than inventing a large system.

Developer note:

{content}
"""

    schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            },
            "goal": {
                "type": "string"
            },
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string"
                        },
                        "actions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "dependencies": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": [
                        "title",
                        "actions",
                        "dependencies"
                    ]
                }
            },
            "verification": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": [
            "title",
            "goal",
            "steps",
            "verification"
        ]
    }

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
            temperature=0.2
        )
    )

    try:
        return json.loads(response.text)

    except (json.JSONDecodeError, TypeError) as exc:
        raise RuntimeError(
            "The AI returned an invalid plan."
        ) from exc