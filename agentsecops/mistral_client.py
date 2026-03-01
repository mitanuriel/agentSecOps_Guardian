"""
Mistral AI API Client

This module provides integration with Mistral AI's chat completions API for security analysis.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from .promptregistry import get_prompt, get_security_advisor_guidance


class MistralClient:
    """Client for interacting with Mistral AI's chat completions API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Mistral client.

        Args:
            api_key: Mistral API key. If not provided, will look for MISTRAL_API_KEY in environment.
        """
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Mistral API key not provided and MISTRAL_API_KEY environment variable not set"
            )

        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def analyze_with_mistral(
        self,
        text: str,
        analysis_type: str = "security_analysis",
        security_findings: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Analyze text using Mistral AI with the specified analysis type.

        Args:
            text: Text to analyze
            analysis_type: Type of analysis to perform (prompt_injection, hallucination, security_analysis, etc.)
            security_findings: Optional security findings from pattern matching

        Returns:
            Dictionary containing the analysis results
        """
        # Get the appropriate system prompt
        system_prompt = get_prompt(analysis_type)

        # Format the prompt with the text and optional findings
        prompt_vars = {"text": text}
        if security_findings:
            prompt_vars["security_findings"] = json.dumps(security_findings, indent=2)

        formatted_prompt = system_prompt.format(**prompt_vars)
        advisor_guidance = get_security_advisor_guidance()
        if advisor_guidance and analysis_type in {
            "prompt_injection",
            "security_analysis",
            "secure_coding",
        }:
            formatted_prompt = (
                f"{formatted_prompt}\n\nSecurity advisor guidance:\n{advisor_guidance}"
            )

        # Prepare the request payload
        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a security analysis assistant. Respond only in valid JSON format.",
                },
                {"role": "user", "content": formatted_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 1000,
            "response_format": {"type": "json_object"},
        }

        try:
            # Make the API request
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)

            response.raise_for_status()

            # Parse and return the response
            result = response.json()

            # Extract the content from the response
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0]["message"]["content"]
                try:
                    # Parse the JSON response
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If JSON parsing fails, return the raw content
                    return {
                        "error": "Failed to parse Mistral response as JSON",
                        "raw_response": content,
                        "full_api_response": result,
                    }
            else:
                return {"error": "No valid response from Mistral API", "full_api_response": result}

        except requests.exceptions.RequestException as e:
            return {
                "error": f"Mistral API request failed: {str(e)}",
                "exception_type": type(e).__name__,
            }
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}", "exception_type": type(e).__name__}

    def analyze_prompt_injection(self, text: str) -> Dict[str, Any]:
        """Analyze text for prompt injection attempts."""
        return self.analyze_with_mistral(text, "prompt_injection")

    def analyze_hallucination_risk(self, text: str) -> Dict[str, Any]:
        """Analyze text for hallucination risks."""
        return self.analyze_with_mistral(text, "hallucination")

    def analyze_security(self, text: str, security_findings: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive security analysis."""
        return self.analyze_with_mistral(text, "security_analysis", security_findings)

    def get_secure_coding_recommendations(
        self, text: str, security_findings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get secure coding recommendations."""
        return self.analyze_with_mistral(text, "secure_coding", security_findings)

    def analyze_compliance(self, text: str) -> Dict[str, Any]:
        """Analyze text for compliance with security standards."""
        return self.analyze_with_mistral(text, "compliance")


def analyze_with_mistral_api(
    text: str,
    api_key: Optional[str] = None,
    analysis_type: str = "security_analysis",
    security_findings: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Convenience function to analyze text with Mistral AI without creating a client instance.

    Args:
        text: Text to analyze
        api_key: Mistral API key (optional)
        analysis_type: Type of analysis to perform
        security_findings: Optional security findings from pattern matching

    Returns:
        Dictionary containing the analysis results
    """
    try:
        client = MistralClient(api_key)
        return client.analyze_with_mistral(text, analysis_type, security_findings)
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Failed to initialize Mistral client: {str(e)}"}
