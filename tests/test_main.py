"""Tests for the main orchestrator module."""

import tempfile
import os
from pathlib import Path
from agentsecops.main import main
from agentsecops.securityinstructions import analyze_security
from agentsecops.reporting import generate_report


def test_main_workflow():
    """Test the complete workflow from file input to report generation."""
    # Create a temporary test file
    test_content = """
    This is a test file with some security issues.
    password = secret123
    api_key = abc123def456ghi789
    user@email.com
    eval("some code")
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name
    
    try:
        # Create a temporary output file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_output:
            temp_output_path = temp_output.name
        
        # Test main function
        import sys
        original_argv = sys.argv.copy()
        sys.argv = ['main.py', temp_file_path, '-o', temp_output_path]
        
        result = main()
        
        # Verify the result
        assert result == 0, "Main function should return 0 on success"
        assert os.path.exists(temp_output_path), "Output file should be created"
        
        # Verify report content
        with open(temp_output_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        assert "# Security Analysis Report" in report_content
        assert "Potential Passwords Found" in report_content
        assert "Security Issues Found" in report_content
        assert "Potential Sensitive Data Found" in report_content
        
    finally:
        # Clean up
        sys.argv = original_argv
        os.unlink(temp_file_path)
        if os.path.exists(temp_output_path):
            os.unlink(temp_output_path)


def test_analyze_security():
    """Test the security analysis function."""
    test_content = """
    password = test123
    api_key = abc123def456ghi789jkl01234567890123456789
    eval("code")
    """
    
    findings = analyze_security(test_content)
    
    # Verify findings structure
    assert 'metadata' in findings
    assert 'findings' in findings
    
    # Verify specific findings
    assert len(findings['findings']['passwords']) > 0
    assert len(findings['findings']['api_keys']) > 0
    assert len(findings['findings']['security_issues']) > 0
    
    # Verify metadata
    assert findings['metadata']['content_length'] > 0
    assert findings['metadata']['line_count'] > 0


def test_generate_report():
    """Test the report generation function."""
    # Create test findings
    test_findings = {
        'metadata': {
            'content_length': 100,
            'line_count': 5
        },
        'findings': {
            'passwords': [
                {'line': 1, 'match': 'password=test', 'context': 'password=test'}
            ],
            'api_keys': [],
            'sensitive_data': [],
            'security_issues': []
        }
    }
    
    # Create temporary output file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as temp_file:
        temp_file_path = temp_file.name
    
    try:
        # Generate report
        generate_report(test_findings, temp_file_path)
        
        # Verify file was created
        assert os.path.exists(temp_file_path)
        
        # Verify content
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "# Security Analysis Report" in content
        assert "Potential Passwords Found (1)" in content
        assert "Line 1" in content
        
    finally:
        # Clean up
        os.unlink(temp_file_path)


def test_empty_content():
    """Test with empty content."""
    findings = analyze_security("")
    
    assert findings['metadata']['content_length'] == 0
    assert findings['metadata']['line_count'] == 0
    assert len(findings['findings']['passwords']) == 0
    assert len(findings['findings']['api_keys']) == 0


def test_no_security_issues():
    """Test with content that has no security issues."""
    clean_content = "This is completely clean content with no issues."
    
    findings = analyze_security(clean_content)
    
    assert len(findings['findings']['passwords']) == 0
    assert len(findings['findings']['api_keys']) == 0
    assert len(findings['findings']['sensitive_data']) == 0
    assert len(findings['findings']['security_issues']) == 0


if __name__ == "__main__":
    test_main_workflow()
    test_analyze_security()
    test_generate_report()
    test_empty_content()
    test_no_security_issues()
    print("All tests passed!")