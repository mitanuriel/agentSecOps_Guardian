"""Simple backend for generating social media posts via Mistral."""

import requests
from fastapi import FastAPI
from pydantic import BaseModel


MISTRAL_CHAT_COMPLETIONS_URL = "https://api.mistral.ai/v1/chat/completions"

app = FastAPI(title="Social Media Manager Backend")


class GeneratePostRequest(BaseModel):
    """Request payload for social media post generation."""

    api_key: str
    prompt: str
    model: str = "mistral-small-latest"


@app.get("/health")
def health() -> dict:
    """Health endpoint for quick service checks."""
    return {"status": "ok"}


@app.post("/generate-post")
def generate_post(payload: GeneratePostRequest) -> dict:
    """Generate a social media post from a user prompt using Mistral."""
    response = requests.post(
        MISTRAL_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {payload.api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": payload.model,
            "messages": [{"role": "user", "content": payload.prompt}],
        },
        timeout=60,
    )
    response.raise_for_status()

    completion = response.json()
    post_text = completion["choices"][0]["message"]["content"]

    return {
        "post": post_text,
        "model": payload.model,
        "provider": "mistral",
    }
