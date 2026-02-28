"""
Main CLI tool for AgentSecOps Guardian - 'secure' command

This module provides a comprehensive CLI tool for security analysis of text files
with optional Mistral AI integration for advanced threat detection.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Local imports
from .parsing.textfile import read_text_file, parse_text
from .securityinstructions import analyze_security
from .reporting import generate_report
from .mistral_client import MistralClient, analyze_with_mistral_api


def main():
    """Main entry point for the 'secure' CLI tool."""
    parser = argparse.ArgumentParser(
        description="secure - AI-Powered Security Analysis Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='secure'
    )

    # Required arguments
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input text file to analyze'
    )

    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='report.md',
        help='Output report file path'
    )

    # Text processing options
    parser.add_argument(
        '-l', '--lowercase',
        action='store_true',
        help='Convert text to lowercase before analysis'
    )
    parser.add_argument(
        '-s', '--strip',
        action='store_true',
        help='Strip leading/trailing whitespace'
    )
    parser.add_argument(
        '-w', '--remove-whitespace',
        action='store_true',
        help='Remove extra whitespace between words'
    )
    parser.add_argument(
        '--lines',
        action='store_true',
        help='Process line by line (removes empty lines)'
    )

    # Mistral AI integration options
    parser.add_argument(
        '--mistral',
        action='store_true',
        help='Enable Mistral AI analysis for advanced threat detection'
    )
    parser.add_argument(
        '--mistral-key',
        type=str,
        help='Mistral API key (overrides MISTRAL_API_KEY environment variable)'
    )
    parser.add_argument(
        '--analysis-type',
        type=str,
        default='security_analysis',
        choices=['prompt_injection', 'hallucination', 'security_analysis', 'secure_coding', 'compliance'],
        help='Type of Mistral AI analysis to perform'
    )

    # Advanced options
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--no-patterns',
        action='store_true',
        help='Skip pattern-based security analysis'
    )

    args = parser.parse_args()

    try:
        # Step 1: Read and parse the input file
        if args.verbose:
            print(f"📖 Reading and parsing: {args.input_file}")
        
        content = read_text_file(args.input_file)
        parsed_content = parse_text(content, args)

        # Step 2: Pattern-based security analysis (unless disabled)
        security_findings = {}
        if not args.no_patterns:
            if args.verbose:
                print("🔍 Performing pattern-based security analysis...")
            security_findings = analyze_security(parsed_content)
        else:
            if args.verbose:
                print("⚠️  Skipping pattern-based security analysis as requested")

        # Step 3: Mistral AI analysis (if enabled)
        mistral_analysis = {}
        if args.mistral:
            if args.verbose:
                print("🤖 Performing Mistral AI analysis...")
            
            # Get API key from args or environment
            api_key = args.mistral_key or os.environ.get('MISTRAL_API_KEY')
            if not api_key:
                print("❌ Error: Mistral AI analysis requested but no API key provided.")
                print("   Set MISTRAL_API_KEY environment variable or use --mistral-key option.")
                return 1
            
            try:
                mistral_analysis = analyze_with_mistral_api(
                    parsed_content,
                    api_key,
                    args.analysis_type,
                    security_findings if security_findings else None
                )
                
                if 'error' in mistral_analysis:
                    print(f"⚠️  Mistral AI analysis error: {mistral_analysis['error']}")
                    mistral_analysis = {}
                else:
                    if args.verbose:
                        print("✅ Mistral AI analysis completed successfully")
            except Exception as e:
                print(f"⚠️  Mistral AI analysis failed: {str(e)}")
                mistral_analysis = {}

        # Step 4: Generate comprehensive report
        if args.verbose:
            print(f"📊 Generating report: {args.output}")
        
        # Create enhanced findings with both pattern and AI analysis
        enhanced_findings = {
            'metadata': security_findings.get('metadata', {}) if security_findings else {},
            'pattern_analysis': security_findings.get('findings', {}) if security_findings else {},
            'mistral_analysis': mistral_analysis
        }
        
        generate_report(enhanced_findings, args.output)

        if args.verbose:
            print(f"✅ Security analysis complete. Report saved to: {args.output}")
        else:
            print(f"📋 Report generated: {args.output}")

        return 0

    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.input_file}")
        return 1
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())