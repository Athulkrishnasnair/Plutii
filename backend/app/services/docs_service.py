import json
import logging
import os
import re

logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "gemini-3.5-flash-lite"

# Gemini prompt
_SYSTEM_INSTRUCTION = (
    "You are a developer documentation assistant embedded in a developer workflow tool. "
    "Your job is to help developers understand technical documentation quickly. "
    "Base every claim strictly on the supplied documentation. "
    "Do not invent APIs, parameters, behavior, examples, or features that are not "
    "supported by the supplied content. "
    "If the documentation does not contain enough information, say so instead of guessing. "
    "Be concise and practical. "
    "Respond with ONLY a valid JSON object with no markdown fences or extra text."
)

_PROMPT_TEMPLATE = """\
Explain the following technical documentation for a developer.

Return ONLY a JSON object in exactly this shape:

{{
    "summary": "<concise explanation of what the documentation is about>",
    "key_concepts": [
        "<important concept from the documentation>",
        "<another important concept>"
    ],
    "example": "<simple example based only on the supplied documentation>",
    "common_mistake": "<a likely mistake that can be identified from the supplied documentation>"
}}

Rules:
- Use only the supplied documentation.
- Do not invent APIs, methods, parameters, or behavior.
- Keep the explanation concise.
- Make the example directly relevant to the documentation.
- If something cannot be determined from the documentation, say so.
- Return ONLY the JSON object.

---
DOCUMENTATION:
{content}
---

Respond with ONLY the JSON object.
"""

# Prompt function
def _build_prompt(content: str) -> str:
    return _PROMPT_TEMPLATE.format(
        content=content or "(no documentation provided)"
    )

# JSON extraction
def _extract_json(raw: str) -> str:
    fenced = re.sub(
        r"^```(?:json)?\s*",
        "",
        raw.strip(),
        flags=re.IGNORECASE,
    )

    fenced = re.sub(
        r"\s*```$",
        "",
        fenced.strip(),
    )

    return fenced.strip()



# Validate gemini's output
# If geminis output doesnt follow guildlines reject it
def _validate_result(data: dict) -> dict:
    required = {
        "summary",
        "key_concepts",
        "example",
        "common_mistake",
    }

    missing = required - data.keys()

    # Validate 
    if missing:
        raise ValueError(
            f"Response missing required keys: {missing}"
        )

    if not isinstance(data["summary"], str):
        raise ValueError("Field 'summary' must be string")

    if not isinstance(data["key_concepts"], list):
        raise ValueError("Field 'key_concepts' must be a list")

    if not all(isinstance(item, str) for item in data["key_concepts"]):
        raise ValueError(
            "All items in 'key_concepts' must be strings"
        )

    if not isinstance(data["example"], str):
        raise ValueError("Field 'example' must be a string")

    if not isinstance(data["common_mistake"], str):
        raise ValueError(
            "Field 'common_mistake' must be a string"
        )

    return {
        "summary": data["summary"],
        "key_concepts": data["key_concepts"],
        "example": data["example"],
        "common_mistake": data["common_mistake"]
    }


# Calling gemini api
def analyze_docs(content: str) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    # Validate it
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is not set")
        raise RuntimeError(
            "The AI analysis service is not configured. "
            "Please contact the administrator."
        )

    # Get model
    model = (
        os.environ.get("GEMINI_MODEL", "").strip()
        or _DEFAULT_MODEL
    )

    prompt = _build_prompt(content)

    # Send to API
    try: 
        import google.genai as genai
        from google.genai import types as genai_types

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=_SYSTEM_INSTRUCTION,
                temperature=0.2,
            ),
        )

        raw_text = response.text

    except Exception as exc:
        logger.exception("Gemini Docs Lens call failed: %s", exc)

        raise RuntimeError(
            "The AI analysis service is temporarily unavailable. "
            "Please try again later."
        ) from exc

    try:
        cleaned = _extract_json(raw_text)
        data = json.loads(cleaned)

        return _validate_result(data)

    except (json.JSONDecodeError, ValueError) as exc:
        logger.error(
            "Gemini returned invalid Docs Lens JSON. "
            "Model: %s | Error: %s | Raw response: %.500s",
            model,
            exc,
            raw_text,
        )

        raise RuntimeError(
            "The AI analysis service returned an unexpected response. "
            "Please try again."
        ) from exc