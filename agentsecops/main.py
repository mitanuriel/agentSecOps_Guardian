"""
Main orchestrator for AgentSecOps Guardian

This module coordinates text parsing, security analysis, and reporting.
"""

import argparse
from pathlib import Path
from .parsing.textfile import read_text_file, parse_text
from .securityinstructions import analyze_security
from .reporting import generate_report


def main():
    """Main entry point for AgentSecOps Guardian."""
    parser = argparse.ArgumentParser(
        description="AgentSecOps Guardian - Security Analysis Tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Required arguments
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to the input text file'
    )

    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output report file path (default: report.md)'
    )

    # Processing options
    parser.add_argument(
        '-l', '--lowercase',
        action='store_true',
        help='Convert text to lowercase'
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

    args = parser.parse_args()

    try:
        # Step 1: Read and parse the input file
        print(f"Reading and parsing: {args.input_file}")
        content = read_text_file(args.input_file)
        parsed_content = parse_text(content, args)

        # Step 2: Analyze security instructions
        print("Analyzing security instructions...")
        security_findings = analyze_security(parsed_content)

        # Step 3: Generate report
        output_path = args.output if args.output else "report.md"
        print(f"Generating report: {output_path}")
        generate_report(security_findings, output_path)

        print(f"✓ Security analysis complete. Report saved to: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())