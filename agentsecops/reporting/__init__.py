"""
Reporting Module

This module provides functionality to generate security reports in markdown format.
"""

from typing import Dict, Any
from pathlib import Path
import datetime
import json


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
    
    # Pattern-based analysis section
    pattern_analysis = findings.get('pattern_analysis', {})
    if pattern_analysis:
        content.append(f"## 🔍 Pattern-Based Security Analysis\n")
        
        # Passwords section
        passwords = pattern_analysis.get('passwords', [])
        if passwords:
            content.append(f"### 🔴 Potential Passwords Found ({len(passwords)})\n")
            for finding in passwords:
                content.append(f"**Line {finding.get('line', 'Unknown')}:** `{finding.get('match', '')}`\n")
                content.append(f"**Context:** `{finding.get('context', '')}`\n")
                content.append(f"\n")
        
        # API Keys section
        api_keys = pattern_analysis.get('api_keys', [])
        if api_keys:
            content.append(f"### 🔴 Potential API Keys Found ({len(api_keys)})\n")
            for finding in api_keys:
                content.append(f"**Line {finding.get('line', 'Unknown')}:** `{finding.get('match', '')}`\n")
                content.append(f"**Context:** `{finding.get('context', '')}`\n")
                content.append(f"\n")
        
        # Sensitive Data section
        sensitive_data = pattern_analysis.get('sensitive_data', [])
        if sensitive_data:
            content.append(f"### 🔴 Potential Sensitive Data Found ({len(sensitive_data)})\n")
            for finding in sensitive_data:
                content.append(f"**Line {finding.get('line', 'Unknown')}:** `{finding.get('match', '')}`\n")
                content.append(f"**Context:** `{finding.get('context', '')}`\n")
                content.append(f"\n")
        
        # Security Issues section
        security_issues = pattern_analysis.get('security_issues', [])
        if security_issues:
            content.append(f"### 🔴 Security Issues Found ({len(security_issues)})\n")
            for finding in security_issues:
                content.append(f"**Line {finding.get('line', 'Unknown')}:** {finding.get('issue', '')}\n")
                content.append(f"**Context:** `{finding.get('context', '')}`\n")
                content.append(f"\n")
        
        content.append(f"\n---\n")
    
    # Mistral AI analysis section
    mistral_analysis = findings.get('mistral_analysis', {})
    if mistral_analysis:
        content.append(f"## 🤖 Mistral AI Analysis\n")
        
        # Handle different analysis types
        if 'prompt_injection_detected' in mistral_analysis:
            content.append(f"### Prompt Injection Analysis\n")
            content.append(f"- **Detected:** {mistral_analysis.get('prompt_injection_detected', False)}\n")
            content.append(f"- **Confidence:** {mistral_analysis.get('confidence_score', 0):.2f}\n")
            if mistral_analysis.get('vulnerabilities_found'):
                content.append(f"- **Vulnerabilities:** {', '.join(mistral_analysis['vulnerabilities_found'])}\n")
            if mistral_analysis.get('analysis'):
                content.append(f"\n**Analysis:**\n\n{mistral_analysis['analysis']}\n\n")
            if mistral_analysis.get('recommendations'):
                content.append(f"**Recommendations:**\n\n" + "\n".join([f"- {rec}" for rec in mistral_analysis['recommendations']]) + "\n\n")
        
        elif 'hallucination_risk_detected' in mistral_analysis:
            content.append(f"### Hallucination Risk Analysis\n")
            content.append(f"- **Risk Detected:** {mistral_analysis.get('hallucination_risk_detected', False)}\n")
            content.append(f"- **Confidence:** {mistral_analysis.get('confidence_score', 0):.2f}\n")
            if mistral_analysis.get('risk_factors'):
                content.append(f"- **Risk Factors:** {', '.join(mistral_analysis['risk_factors'])}\n")
            if mistral_analysis.get('analysis'):
                content.append(f"\n**Analysis:**\n\n{mistral_analysis['analysis']}\n\n")
            if mistral_analysis.get('recommendations'):
                content.append(f"**Recommendations:**\n\n" + "\n".join([f"- {rec}" for rec in mistral_analysis['recommendations']]) + "\n\n")
        
        elif 'overall_security_score' in mistral_analysis:
            content.append(f"### Comprehensive Security Analysis\n")
            content.append(f"- **Overall Score:** {mistral_analysis.get('overall_security_score', 0):.2f}/1.0\n")
            
            critical = mistral_analysis.get('critical_issues', [])
            medium = mistral_analysis.get('medium_issues', [])
            low = mistral_analysis.get('low_issues', [])
            
            content.append(f"- **Critical Issues:** {len(critical)}\n")
            content.append(f"- **Medium Issues:** {len(medium)}\n")
            content.append(f"- **Low Issues:** {len(low)}\n")
            
            if critical:
                content.append(f"\n**Critical Issues:**\n")
                for issue in critical:
                    content.append(f"- {issue}\n")
            
            if medium:
                content.append(f"\n**Medium Issues:**\n")
                for issue in medium:
                    content.append(f"- {issue}\n")
            
            if low:
                content.append(f"\n**Low Issues:**\n")
                for issue in low:
                    content.append(f"- {issue}\n")
            
            if mistral_analysis.get('detailed_analysis'):
                content.append(f"\n**Detailed Analysis:**\n\n{mistral_analysis['detailed_analysis']}\n\n")
            
            if mistral_analysis.get('remediation_recommendations'):
                content.append(f"**Remediation Recommendations:**\n\n" + "\n".join([f"- {rec}" for rec in mistral_analysis['remediation_recommendations']]) + "\n\n")
        
        elif 'immediate_actions' in mistral_analysis:
            content.append(f"### Secure Coding Recommendations\n")
            
            categories = ['immediate_actions', 'code_refactoring', 'configuration_changes', 'monitoring_recommendations', 'training_recommendations']
            
            for category in categories:
                if mistral_analysis.get(category):
                    display_name = category.replace('_', ' ').title()
                    content.append(f"\n**{display_name}:**\n")
                    for item in mistral_analysis[category]:
                        content.append(f"- {item}\n")
        
        elif any(key in mistral_analysis for key in ['gdpr_compliance', 'pci_dss_compliance', 'hipaa_compliance']):
            content.append(f"### Compliance Analysis\n")
            
            compliance_standards = ['gdpr_compliance', 'pci_dss_compliance', 'hipaa_compliance']
            for standard in compliance_standards:
                if standard in mistral_analysis:
                    compliance_data = mistral_analysis[standard]
                    standard_name = standard.replace('_compliance', '').upper()
                    content.append(f"\n**{standard_name} Compliance:** {'✅ Compliant' if compliance_data.get('compliant', False) else '❌ Not Compliant'}\n")
                    if compliance_data.get('issues'):
                        content.append(f"**Issues:**\n")
                        for issue in compliance_data['issues']:
                            content.append(f"- {issue}\n")
            
            if mistral_analysis.get('owasp_top_10_violations'):
                content.append(f"\n**OWASP Top 10 Violations:**\n")
                for violation in mistral_analysis['owasp_top_10_violations']:
                    content.append(f"- {violation}\n")
            
            if mistral_analysis.get('compliance_recommendations'):
                content.append(f"\n**Compliance Recommendations:**\n")
                for rec in mistral_analysis['compliance_recommendations']:
                    content.append(f"- {rec}\n")
        
        else:
            # Generic JSON display for other analysis types
            content.append(f"### Mistral AI Analysis Results\n")
            content.append(f"```json\n{json.dumps(mistral_analysis, indent=2)}\n```\n")
        
        content.append(f"\n---\n")
    
    # Summary section
    content.append(f"## 📊 Summary\n")
    
    # Count pattern findings
    pattern_findings = pattern_analysis
    pattern_total = 0
    if pattern_findings:
        pattern_total = (len(pattern_findings.get('passwords', [])) +
                        len(pattern_findings.get('api_keys', [])) +
                        len(pattern_findings.get('sensitive_data', [])) +
                        len(pattern_findings.get('security_issues', [])))
    
    content.append(f"- **Pattern-Based Findings:** {pattern_total}\n")
    
    if pattern_findings:
        content.append(f"  - Passwords: {len(pattern_findings.get('passwords', []))}\n")
        content.append(f"  - API Keys: {len(pattern_findings.get('api_keys', []))}\n")
        content.append(f"  - Sensitive Data: {len(pattern_findings.get('sensitive_data', []))}\n")
        content.append(f"  - Security Issues: {len(pattern_findings.get('security_issues', []))}\n")
    
    # Mistral analysis summary
    if mistral_analysis:
        content.append(f"- **Mistral AI Analysis:** ✅ Completed\n")
        
        # Try to extract meaningful metrics based on analysis type
        if 'overall_security_score' in mistral_analysis:
            content.append(f"  - Security Score: {mistral_analysis['overall_security_score']:.2f}/1.0\n")
            content.append(f"  - Critical Issues: {len(mistral_analysis.get('critical_issues', []))}\n")
            content.append(f"  - Medium Issues: {len(mistral_analysis.get('medium_issues', []))}\n")
            content.append(f"  - Low Issues: {len(mistral_analysis.get('low_issues', []))}\n")
        elif 'prompt_injection_detected' in mistral_analysis:
            content.append(f"  - Prompt Injection Detected: {mistral_analysis['prompt_injection_detected']}\n")
            content.append(f"  - Confidence: {mistral_analysis.get('confidence_score', 0):.2f}\n")
        elif 'hallucination_risk_detected' in mistral_analysis:
            content.append(f"  - Hallucination Risk Detected: {mistral_analysis['hallucination_risk_detected']}\n")
            content.append(f"  - Confidence: {mistral_analysis.get('confidence_score', 0):.2f}\n")
    else:
        content.append(f"- **Mistral AI Analysis:** ❌ Not performed\n")
    
    # Final recommendation
    total_findings = pattern_total + (1 if mistral_analysis else 0)
    
    if total_findings > 0:
        content.append(f"\n⚠️  **Recommendation:** Review the findings above and address any genuine security issues.\n")
        if mistral_analysis and 'remediation_recommendations' in mistral_analysis:
            content.append(f"**Top Remediation Recommendations:**\n")
            recommendations = mistral_analysis['remediation_recommendations'][:3]  # Top 3
            for rec in recommendations:
                content.append(f"- {rec}\n")
    else:
        content.append(f"\n✅ **No security issues detected.**\n")
    
    return ''.join(content)