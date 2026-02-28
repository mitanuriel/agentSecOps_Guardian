"""Minimal local test script for the social media backend function."""

import os

from src.social_media_backend import GeneratePostRequest, generate_post


def main() -> None:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing MISTRAL_API_KEY. Example:\n"
            "export MISTRAL_API_KEY='your-key-here'\n"
            "python example_backend.py"
        )

    payload = GeneratePostRequest(
        api_key=api_key,
        prompt="generate twitter post about weather",
        model="mistral-small-latest",
    )

    result = generate_post(payload)
    print(result)


if __name__ == "__main__":
    main()
