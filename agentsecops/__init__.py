"""
AgentSecOps Guardian - AI-Powered Security Analysis Tool

This package provides comprehensive security analysis capabilities for text files,
including pattern-based vulnerability detection and optional Mistral AI integration
for advanced threat analysis.
"""

__version__ = "0.1.0"
__author__ = "AgentSecOps Team"
__email__ = "security@agentsecops.ai"
__license__ = "MIT"
__copyright__ = "Copyright 2026, AgentSecOps Team"

# Import main modules for easy access
from .main import main
from .mistral_client import MistralClient, analyze_with_mistral_api
from .securityinstructions import analyze_security
from .parsing.textfile import read_text_file, parse_text
from .reporting import generate_report
from .promptregistry import (
    PROMPT_INJECTION_DETECTION,
    HALLUCINATION_RISK_DETECTION,
    SECURITY_ANALYSIS,
    SECURE_CODING_RECOMMENDATIONS,
    COMPLIANCE_ANALYSIS,
    get_prompt,
)

__all__ = [
    "main",
    "MistralClient",
    "analyze_with_mistral_api",
    "analyze_security",
    "read_text_file",
    "parse_text",
    "generate_report",
    "PROMPT_INJECTION_DETECTION",
    "HALLUCINATION_RISK_DETECTION",
    "SECURITY_ANALYSIS",
    "SECURE_CODING_RECOMMENDATIONS",
    "COMPLIANCE_ANALYSIS",
    "get_prompt",
]
