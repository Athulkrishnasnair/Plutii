import json
import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


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

    response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    text = response.text.strip()

    print("GEMINI RESPONSE:")
    print(text)


    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)