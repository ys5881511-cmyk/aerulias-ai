from openai import OpenAI
import json
import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_local_env():
    env_path = PROJECT_ROOT / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def get_openrouter_client():
    load_local_env()

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY environment variable.")

    return OpenAI(
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=api_key,
        default_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
            "X-Title": os.getenv("OPENROUTER_APP_NAME", "aerulias_ai")
        }
    )


def get_model():
    load_local_env()
    return os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")


def parse_json_response(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").removesuffix("```").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").removesuffix("```").strip()

    return json.loads(text)


def chat_json(prompt, temperature=0.2):
    client = get_openrouter_client()

    response = client.chat.completions.create(
        model=get_model(),
        messages=[
            {"role": "system", "content": "You return only valid JSON. No markdown."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=temperature
    )

    return parse_json_response(response.choices[0].message.content)
