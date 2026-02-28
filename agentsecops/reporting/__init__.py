"""
Reporting Module

This module provides functionality to generate security reports in markdown format.
"""

from typing import Dict, Any
from pathlib import Path
import datetime


def generate_report(findings: Dict[str, Any], output_path: str = "report.md") -> None:
    """
    Generate a markdown security report from analysis findings.
    
    Args:
        findings: Dictionary containing security findings
        output_path: Path to save the markdown report
    """
    report_content = _generate_report_content(findings)
    
    # Ensure output directory exists
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)


def _generate_report_content(findings: Dict[str, Any]) -> str:
    """Generate the markdown content for the security report."""
    report_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = []
    content.append(f"# Security Analysis Report\n")
    content.append(f"**Generated:** {report_date}\n")
    content.append(f"\n---\n")
    
    # Metadata section
    content.append(f"## Analysis Metadata\n")
    metadata = findings.get('metadata', {})
    content.append(f"- **Content Length:** {metadata.get('content_length', 0)} characters\n")
    content.append(f"- **Line Count:** {metadata.get('line_count', 0)} lines\n")
    content.append(f"\n---\n")
    
    # Findings sections
    findings_data = findings.get('findings', {})
    
    # Passwords section
    passwords = findings_data.get('passwords', [])
    if passwords:
        content.append(f"## 🔴 Potential Passwords Found ({len(passwords)})\n")
        for finding in passwords:
            content.append(f"### Line {finding.get('line', 'Unknown')}\n")
            content.append(f"**Match:** `{finding.get('match', '')}`\n")
            content.append(f"**Context:** `{finding.get('context', '')}`\n")
            content.append(f"\n")
        content.append(f"\n---\n")
    
    # API Keys section
    api_keys = findings_data.get('api_keys', [])
    if api_keys:
        content.append(f"## 🔴 Potential API Keys Found ({len(api_keys)})\n")
        for finding in api_keys:
            content.append(f"### Line {finding.get('line', 'Unknown')}\n")
            content.append(f"**Match:** `{finding.get('match', '')}`\n")
            content.append(f"**Context:** `{finding.get('context', '')}`\n")
            content.append(f"\n")
        content.append(f"\n---\n")
    
    # Sensitive Data section
    sensitive_data = findings_data.get('sensitive_data', [])
    if sensitive_data:
        content.append(f"## 🔴 Potential Sensitive Data Found ({len(sensitive_data)})\n")
        for finding in sensitive_data:
            content.append(f"### Line {finding.get('line', 'Unknown')}\n")
            content.append(f"**Match:** `{finding.get('match', '')}`\n")
            content.append(f"**Context:** `{finding.get('context', '')}`\n")
            content.append(f"\n")
        content.append(f"\n---\n")
    
    # Security Issues section
    security_issues = findings_data.get('security_issues', [])
    if security_issues:
        content.append(f"## 🔴 Security Issues Found ({len(security_issues)})\n")
        for finding in security_issues:
            content.append(f"### Line {finding.get('line', 'Unknown')}\n")
            content.append(f"**Issue:** {finding.get('issue', '')}\n")
            content.append(f"**Context:** `{finding.get('context', '')}`\n")
            content.append(f"\n")
        content.append(f"\n---\n")
    
    # Summary section
    total_findings = len(passwords) + len(api_keys) + len(sensitive_data) + len(security_issues)
    content.append(f"## 📊 Summary\n")
    content.append(f"- **Total Findings:** {total_findings}\n")
    content.append(f"- **Passwords:** {len(passwords)}\n")
    content.append(f"- **API Keys:** {len(api_keys)}\n")
    content.append(f"- **Sensitive Data:** {len(sensitive_data)}\n")
    content.append(f"- **Security Issues:** {len(security_issues)}\n")
    
    if total_findings > 0:
        content.append(f"\n⚠️  **Recommendation:** Review the findings above and address any genuine security issues.\n")
    else:
        content.append(f"\n✅ **No security issues detected.**\n")
    
    return ''.join(content)