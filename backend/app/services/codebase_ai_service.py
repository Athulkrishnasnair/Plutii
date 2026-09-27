import json
import os


def _get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not configured.")
    import google.genai as genai
    return genai.Client(api_key=api_key)


def _get_model():
    return os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def _clean_json_text(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "")
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()
    return cleaned


def analyze_codebase(query, files):
    context_parts = []

    for file in files:
        context_parts.append(
            f"""
FILE: {file["path"]}

{file["content"]}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are ArrowLens Codebase Lens.

Analyze the provided project source code to answer the user's question.

USER QUESTION:
{query}

PROJECT FILES:
{context}

Return ONLY valid JSON:

{{
  "answer": "A concise explanation.",
  "files": [
    {{
      "path": "path/to/file",
      "reason": "Why this file is relevant."
    }}
  ]
}}

Rules:
- Base your answer only on the provided project.
- Do not invent files.
- Mention the most relevant files first.
- Keep the explanation practical.
"""

    client = _get_client()
    response = client.models.generate_content(
        model=_get_model(),
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    cleaned = _clean_json_text(response.text)
    return json.loads(cleaned)


def explain_file(file_path: str, content: str, related_relationships=None):
    """
    Analyze and explain an entire source file:
    - Purpose
    - What the file does
    - Important dependencies
    - Inputs/outputs
    - Architecture fit
    - Modification caveats
    """
    rel_info = ""
    if related_relationships:
        rel_info = "\nKNOWN IMPORT RELATIONSHIPS:\n" + "\n".join(
            f"- {r.get('source')} -> {r.get('target')}" for r in related_relationships
        )

    prompt = f"""
You are ArrowLens Codebase Lens. Explain the provided source file clearly to a developer.

FILE: {file_path}
{rel_info}

SOURCE CODE:
{content}

Provide a structured, technical explanation of this file.
Return ONLY valid JSON in this exact shape:

{{
  "scope": "file",
  "file_path": "{file_path}",
  "purpose": "1-2 sentence core purpose of this file.",
  "what_it_does": "Detailed breakdown of what this file accomplishes.",
  "dependencies": ["Key dependency or imported module 1", "Key dependency 2"],
  "inputs_outputs": "Inputs, arguments accepted, and exported symbols, classes, or components.",
  "architecture_fit": "How this file fits into the overall codebase architecture.",
  "modification_notes": "Important considerations, invariants, or pitfalls to know before modifying this file."
}}

Rules:
- Base your explanation strictly on the provided source code.
- Do not hallucinate imports or functions that are not present.
- Keep explanations clear, practical, and developer-oriented.
"""

    client = _get_client()
    response = client.models.generate_content(
        model=_get_model(),
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    cleaned = _clean_json_text(response.text)
    return json.loads(cleaned)


def explain_selection(
    file_path: str,
    selected_code: str,
    start_line: int,
    end_line: int,
    surrounding_context: str = "",
    related_relationships=None
):
    """
    Analyze and explain a specific selected range of lines within a file.
    Focuses primarily on the selected lines, using surrounding context only to clarify.
    """
    prompt = f"""
You are ArrowLens Codebase Lens.

The developer wants to understand this specific section of code. Focus primarily on the selected lines. Use surrounding context only to explain how the selected code works.

FILE: {file_path}
SELECTED LINES: {start_line} to {end_line}

SELECTED CODE:
{selected_code}

SURROUNDING FILE CONTEXT:
{surrounding_context}

Return ONLY valid JSON in this exact shape:

{{
  "scope": "selection",
  "file_path": "{file_path}",
  "start_line": {start_line},
  "end_line": {end_line},
  "selected_code": {json.dumps(selected_code)},
  "what_it_does": "Clear description of what this selected section of code does.",
  "how_it_works": "Technical step-by-step breakdown of the logic.",
  "why_it_exists": "Why this block exists in the context of the module.",
  "dependencies_context": "Key variables, parameters, imports, or state this section relies upon.",
  "modification_notes": "Important considerations, potential side-effects, or invariants if editing this section."
}}

Rules:
- Focus primarily on the selected lines.
- Do not rewrite the code or provide unsolicited solutions.
- Keep explanations practical and directly grounded in the code.
"""

    client = _get_client()
    response = client.models.generate_content(
        model=_get_model(),
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    cleaned = _clean_json_text(response.text)
    return json.loads(cleaned)