"""Simple backend for generating social media posts via Mistral."""

import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

MISTRAL_CHAT_COMPLETIONS_URL = "https://api.mistral.ai/v1/chat/completions"

app = FastAPI(title="Social Media Manager Backend")

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


class GeneratePostRequest(BaseModel):
    """Request payload for social media post generation."""

    api_key: str
    prompt: str
    model: str = "mistral-small-latest"


@app.get("/")
def index():
    """Serve the frontend dashboard."""
    return FileResponse(str(BASE_DIR / "static" / "index.html"))


@app.get("/health")
def health() -> dict:
    """Health endpoint for quick service checks."""
    return {"status": "ok"}


@app.post("/generate-post")
def generate_post(payload: GeneratePostRequest) -> dict:
    """Generate a social media post from a user prompt using Mistral."""
    try:
        # Clean the API key (remove any whitespace)
        clean_api_key = payload.api_key.strip()

        # Log key format for debugging (first/last 4 chars only)
        key_preview = (
            f"{clean_api_key[:4]}...{clean_api_key[-4:]}" if len(clean_api_key) > 8 else "***"
        )
        print(f"DEBUG: Using API key: {key_preview}, length: {len(clean_api_key)}")

        response = requests.post(
            MISTRAL_CHAT_COMPLETIONS_URL,
            headers={
                "Authorization": f"Bearer {clean_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": payload.model,
                "messages": [{"role": "user", "content": payload.prompt}],
            },
            timeout=60,
        )

        # Handle API errors with helpful messages
        if response.status_code == 401:
            from fastapi import HTTPException

            error_msg = response.json().get("message", "") if response.text else ""
            print(f"DEBUG: 401 error details - {error_msg}")
            raise HTTPException(
                status_code=401,
                detail=f"Invalid API key. Check: 1) Key is correctly copied from Mistral console 2) No extra spaces 3) Key is activated. API response: {error_msg}",
            )
        elif response.status_code == 429:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=429, detail="Rate limit exceeded. Please wait a moment and try again."
            )
        elif response.status_code >= 400:
            from fastapi import HTTPException

            error_detail = response.json().get("error", {}).get("message", "Unknown error")
            raise HTTPException(
                status_code=response.status_code, detail=f"Mistral API error: {error_detail}"
            )

        response.raise_for_status()

        completion = response.json()
        post_text = completion["choices"][0]["message"]["content"]

        return {
            "post": post_text,
            "model": payload.model,
            "provider": "mistral",
        }

    except requests.exceptions.Timeout:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=504,
            detail="Request timeout. The API took too long to respond. Please try again.",
        )
    except requests.exceptions.RequestException as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")
