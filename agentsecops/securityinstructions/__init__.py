"""
Security Instructions Analysis Module

This module provides security analysis capabilities for text content.
"""

from typing import Dict, List, Any
import re


def analyze_security(content: str) -> Dict[str, Any]:
    """
    Analyze text content for security-related findings.

    Args:
        content: Text content to analyze

    Returns:
        Dictionary containing security findings with categories and issues
    """
    findings = {
        "metadata": {
            "content_length": len(content),
            "line_count": len(content.splitlines()) if content else 0,
        },
        "findings": {"passwords": [], "api_keys": [], "sensitive_data": [], "security_issues": []},
    }

    # Check for common security issues
    lines = content.splitlines() if content else []

    # Pattern 1: Potential passwords
    password_patterns = [
        r"password[\s]*[:=][\s]*[\w\-]+",
        r"passwd[\s]*[:=][\s]*[\w\-]+",
        r"pwd[\s]*[:=][\s]*[\w\-]+",
    ]

    for i, line in enumerate(lines, 1):
        for pattern in password_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                findings["findings"]["passwords"].append(
                    {"line": i, "match": match.group(), "context": line.strip()}
                )

    # Pattern 2: API keys and secrets
    api_key_patterns = [
        r"api[\s]*key[\s]*[:=][\s]*[\w\-]+",
        r"secret[\s]*[:=][\s]*[\w\-]+",
        r"token[\s]*[:=][\s]*[\w\-]+",
        r"[A-Za-z0-9]{32,}",  # Long hex strings
    ]

    for i, line in enumerate(lines, 1):
        for pattern in api_key_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                findings["findings"]["api_keys"].append(
                    {"line": i, "match": match.group(), "context": line.strip()}
                )

    # Pattern 3: Sensitive data patterns
    sensitive_patterns = [
        r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}",  # Credit card numbers
        r"\d{3}[\s-]?\d{2}[\s-]?\d{4}",  # SSN patterns
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email addresses
    ]

    for i, line in enumerate(lines, 1):
        for pattern in sensitive_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                findings["findings"]["sensitive_data"].append(
                    {"line": i, "match": match.group(), "context": line.strip()}
                )

    # Pattern 4: Common security issues
    security_issue_patterns = [
        (r"eval\(", "Use of eval() function"),
        (r"exec\(", "Use of exec() function"),
        (r"pickle\.load", "Use of pickle.load()"),
        (r"http://", "Insecure HTTP protocol"),
        (r"\\\\", "Potential path traversal"),
    ]

    for i, line in enumerate(lines, 1):
        for pattern, description in security_issue_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                findings["findings"]["security_issues"].append(
                    {"line": i, "issue": description, "context": line.strip()}
                )

    return findings
