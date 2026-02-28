#!/usr/bin/env python3
"""Quick test script to validate your Mistral API key."""

import os
import sys
import getpass
import requests

def test_mistral_key(api_key: str) -> None:
    """Test if a Mistral API key is valid."""
    # Clean the key
    api_key = api_key.strip()
    
    # Validate without exposing key content
    if not api_key:
        print("❌ ERROR: API key is empty")
        sys.exit(1)
    
    print("Testing API key...")
    print()
    
    # Test with a simple request
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "mistral-small-latest",
        "messages": [{"role": "user", "content": "Say 'hello'"}],
        "max_tokens": 10
    }
    
    try:
        print("Sending test request to Mistral API...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Your API key is valid and working!")
            result = response.json()
            print(f"Response: {result['choices'][0]['message']['content']}")
        elif response.status_code == 401:
            print("❌ AUTHENTICATION FAILED")
            print(f"Error: {response.text}")
            print("\nPossible issues:")
            print("  1. API key is incorrect or expired")
            print("  2. API key not activated yet (wait a few minutes after redeeming)")
            print("  3. Copy-paste error (check for extra spaces or missing characters)")
            print("\nVerify your key at: https://console.mistral.ai/")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"Details: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("Check your internet connection")

if __name__ == "__main__":
    # Try to get API key from secure sources
    api_key = os.getenv("MISTRAL_API_KEY")
    
    if not api_key:
        # Prompt securely without echoing to terminal
        try:
            api_key = getpass.getpass("Enter your Mistral API key: ")
        except (KeyboardInterrupt, EOFError):
            print("\n❌ API key input cancelled")
            sys.exit(1)
    
    if not api_key or not api_key.strip():
        print("❌ ERROR: No API key provided")
        print("\nSet MISTRAL_API_KEY environment variable:")
        print("  export MISTRAL_API_KEY='your-key-here'")
        print("  python test_api_key.py")
        print("\nOr run the script and enter key when prompted (secure input)")
        sys.exit(1)
    
    test_mistral_key(api_key)
