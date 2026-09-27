import json
import logging
import os
import re

logger = logging.getLogger(__name__)

# Default model — current Gemini 2.0 Flash, fast and capable.
_DEFAULT_MODEL = "gemini-2.0-flash"

# Prompt template sent to Gemini.
_SYSTEM_INSTRUCTION = (
    "You are a developer debugging assistant embedded in a developer workflow tool. "
    "Your job is to help developers understand errors quickly and act on them. "
    "Rules you must follow without exception:\n"
    "1. Base every claim strictly on the supplied ERROR MESSAGE, RELEVANT CODE, "
    "and EXECUTION CONTEXT. Do not invent filenames, variable names, function "
    "names, APIs, stack frames, or application behaviour that were not supplied.\n"
    "2. If a field in your response is supported directly by the supplied "
    "information, state it as fact. If it is inferred, say so explicitly "
    "(e.g. 'likely', 'probably', 'if X is the case').\n"
    "3. If the supplied information is insufficient to give a confident answer "
    "for any field, say what is missing rather than guessing "
    "(e.g. 'Cannot determine cause without the stack trace.').\n"
    "4. Give a concrete fix only when the evidence supports one. "
    "If it does not, describe what the developer should investigate first.\n"
    "5. Verification steps must be specific to this error — "
    "not generic advice like 'run the tests again'.\n"
    "6. Be concise. A developer reading this mid-workflow does not want prose.\n"
    "7. Respond with ONLY a valid JSON object — no markdown fences, "
    "no prose outside the object, no extra keys."
)

_PROMPT_TEMPLATE = """\
A developer has submitted an error for analysis. \
Respond with ONLY a JSON object in exactly this shape:

{{
  "problem":      "<one sentence: what went wrong, based only on the supplied information>",
  "cause":        "<root cause if it can be determined from the supplied information; \
if not, state what is missing — do not invent a cause>",
  "fix":          "<concrete fix tied to the supplied code and error; \
if evidence is insufficient, describe what to investigate rather than guessing>",
  "verification": [
    "<specific, observable step to confirm this exact error is resolved>",
    "<additional step if needed — omit generic steps like 'run your tests'>"
  ]
}}

Use only the information below. Do not invent anything not present in it.

---
ERROR MESSAGE:
{error}

RELEVANT CODE:
{code}

EXECUTION CONTEXT:
{context}
---

Respond with ONLY the JSON object. No markdown. No explanation outside the object.
"""


def _build_prompt(error: str, code: str, context: str) -> str:
    """Fill the prompt template with the caller-supplied values."""
    return _PROMPT_TEMPLATE.format(
        error=error or "(none provided)",
        code=code or "(none provided)",
        context=context or "(none provided)",
    )


def _extract_json(raw: str) -> str:
    """
    Strip markdown code fences that Gemini sometimes wraps around JSON,
    then return the trimmed content ready for json.loads().

    Handles both:
      ```json { ... } ```
      ``` { ... } ```
      plain { ... }
    """
    # Remove ```json ... ``` or ``` ... ``` fences
    fenced = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.IGNORECASE)
    fenced = re.sub(r"\s*```$", "", fenced.strip())
    return fenced.strip()


def _validate_result(data: dict) -> dict:
    """
    Ensure the parsed dict has the four expected keys and correct types.
    Raises ValueError with a descriptive message if validation fails.
    """
    required = {"problem", "cause", "fix", "verification"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Response missing required keys: {missing}")

    for key in ("problem", "cause", "fix"):
        if not isinstance(data[key], str):
            raise ValueError(f"Field '{key}' must be a string")

    if not isinstance(data["verification"], list):
        raise ValueError("Field 'verification' must be a list")

    if not all(isinstance(s, str) for s in data["verification"]):
        raise ValueError("All items in 'verification' must be strings")

    return {
        "problem": data["problem"],
        "cause": data["cause"],
        "fix": data["fix"],
        "verification": data["verification"],
    }


def analyze_error(error: str, code: str = "", context: str = "") -> dict:
    """
    Analyze a developer error using the Google Gemini API.

    Reads configuration from environment variables:
        GEMINI_API_KEY  — required; the Gemini API key.
        GEMINI_MODEL    — optional; defaults to gemini-2.0-flash.

    Returns a dict with keys: problem, cause, fix, verification.
    Raises RuntimeError with a safe, user-facing message on any failure.
    """
    # --- Read configuration from environment ---
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is not set")
        raise RuntimeError(
            "The AI analysis service is not configured. "
            "Please contact the administrator."
        )

    model = os.environ.get("GEMINI_MODEL", "").strip() or _DEFAULT_MODEL

    # --- Build the prompt ---
    prompt = _build_prompt(error=error, code=code, context=context)

    # --- Call Gemini ---
    try:
        import google.genai as genai
        from google.genai import types as genai_types

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=genai_types.GenerateContentConfig(
                system_instruction=_SYSTEM_INSTRUCTION,
                temperature=0.2,  # low temperature → deterministic, structured output
            ),
        )

        raw_text = response.text

    except Exception as exc:
        # Log the real error server-side; return a safe message to the caller.
        logger.exception("Gemini API call failed: %s", exc)
        raise RuntimeError(
            "The AI analysis service is temporarily unavailable. "
            "Please try again later."
        ) from exc

    # --- Parse and validate ---
    try:
        cleaned = _extract_json(raw_text)
        data = json.loads(cleaned)
        return _validate_result(data)

    except (json.JSONDecodeError, ValueError) as exc:
        logger.error(
            "Gemini returned unparseable or invalid JSON. "
            "Model: %s | Error: %s | Raw response: %.500s",
            model, exc, raw_text,
        )
        raise RuntimeError(
            "The AI analysis service returned an unexpected response. "
            "Please try again."
        ) from exc
