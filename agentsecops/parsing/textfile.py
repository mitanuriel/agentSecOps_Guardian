"""
Universal Text File Parser

Usage:
    python text_parser.py <input_file> [options]

Features:
- Reads any text file (txt, csv, json, etc.)
- Returns content as a string
- Optional preprocessing (lowercase, strip whitespace, etc.)
- Line-by-line or full-content processing
"""

import argparse
import json
from pathlib import Path
from typing import Optional, Union
import sys


def read_text_file(file_path: Union[str, Path]) -> str:
    """Read a text file and return its content as a string."""
    
    # check if file_path is provided, if not read from stdin
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encodings if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                raise ValueError(f"Failed to read file: {e}")
        
    else:
        # Read from stdin
        return sys.stdin.read()

def parse_text(content: str, args: argparse.Namespace) -> str:
    """Parse text according to specified options."""
    result = content

    # Apply preprocessing
    if hasattr(args, 'lowercase') and args.lowercase:
        result = result.lower()
    if hasattr(args, 'strip') and args.strip:
        result = result.strip()
    if hasattr(args, 'remove_whitespace') and args.remove_whitespace:
        result = ' '.join(result.split())
    if hasattr(args, 'lines') and args.lines:
        return '\n'.join(line.strip() for line in result.splitlines() if line.strip())

    # Handle JSON if requested
    if hasattr(args, 'parse_json') and args.parse_json:
        try:
            data = json.loads(result)
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            if hasattr(args, 'strict') and args.strict:
                raise ValueError("Invalid JSON format")
            return result  # Return original if not valid JSON

    return result