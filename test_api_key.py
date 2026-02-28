#!/usr/bin/env python3
"""Quick test script to validate your Mistral API key."""

import sys
import requests

def validate_mistral_key(api_key: str) -> None:
    """Validate if a Mistral API key is valid."""
    # Clean the key
    api_key = api_key.strip()
    
    print(f"Testing API key...")
    print(f"  Length: {len(api_key)} characters")
    print(f"  Preview: {api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "  Key too short!")
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
    if len(sys.argv) < 2:
        print("Usage: python test_api_key.py YOUR_API_KEY")
        print("\nOr set MISTRAL_API_KEY environment variable:")
        print("  export MISTRAL_API_KEY='your-key-here'")
        print("  python test_api_key.py")
        
        import os
        api_key = os.getenv("MISTRAL_API_KEY")
        if api_key:
            print("\nFound MISTRAL_API_KEY in environment, testing...")
            validate_mistral_key(api_key)
        else:
            sys.exit(1)
    else:
        validate_mistral_key(sys.argv[1])