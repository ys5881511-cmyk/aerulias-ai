from openai import OpenAI
import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_local_env() -> None:
    """Load environment variables from .env file if it exists."""
    env_path = PROJECT_ROOT / ".env"

    if not env_path.exists():
        logger.debug(".env file not found - using system environment variables")
        return

    try:
        for line in env_path.read_text().splitlines():
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
        logger.info("Successfully loaded .env file")
    except Exception as e:
        logger.warning(f"Error loading .env file: {e}")


def get_openrouter_client() -> OpenAI:
    """Get OpenRouter API client with error handling.
    
    Returns:
        Initialized OpenAI client configured for OpenRouter.
        
    Raises:
        RuntimeError: If OPENROUTER_API_KEY is not set.
    """
    load_local_env()

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        error_msg = "OPENROUTER_API_KEY environment variable is not set"
        logger.error(error_msg)
        raise RuntimeError(error_msg)

    try:
        client = OpenAI(
            base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=api_key,
            default_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
                "X-Title": os.getenv("OPENROUTER_APP_NAME", "aerulias_ai")
            }
        )
        logger.info("OpenRouter client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize OpenRouter client: {e}")
        raise


def get_model() -> str:
    """Get the model name to use from environment.
    
    Returns:
        Model name string, defaults to 'openai/gpt-4o-mini'.
    """
    load_local_env()
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    logger.debug(f"Using model: {model}")
    return model


def parse_json_response(text: str) -> Dict[str, Any]:
    """Parse JSON response with robust error handling for markdown-wrapped JSON.
    
    Args:
        text: Response text that should contain JSON (possibly wrapped in markdown).
        
    Returns:
        Parsed JSON dictionary.
        
    Raises:
        ValueError: If JSON cannot be parsed from the text.
    """
    try:
        text = text.strip()

        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text.removeprefix("```json").removesuffix("```").strip()
        elif text.startswith("```"):
            text = text.removeprefix("```").removesuffix("```").strip()

        result = json.loads(text)
        logger.debug("Successfully parsed JSON response")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}. Text: {text[:100]}")
        raise ValueError(f"Invalid JSON in response: {str(e)}") from e


def chat_json(prompt: str, temperature: float = 0.2) -> Dict[str, Any]:
    """Send a prompt to the model and get JSON response.
    
    Args:
        prompt: User prompt to send to the model.
        temperature: Sampling temperature (0.0 = deterministic, higher = more creative).
        
    Returns:
        Parsed JSON dictionary from model response.
        
    Raises:
        ValueError: If response cannot be parsed as JSON.
        RuntimeError: If API call fails.
    """
    try:
        client = get_openrouter_client()

        logger.debug(f"Sending chat request with temperature={temperature}")
        
        response = client.chat.completions.create(
            model=get_model(),
            messages=[
                {"role": "system", "content": "You return only valid JSON. No markdown."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=temperature
        )

        logger.debug("Received response from OpenRouter")
        return parse_json_response(response.choices[0].message.content)
    except Exception as e:
        logger.error(f"Chat JSON error: {str(e)}")
        raise
