import argparse
import sys
from .parsing.textfile import read_text_file, parse_text

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Universal Text File Parser",
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
        help='Output file path (prints to console if not specified)'
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
    parser.add_argument(
        '-j', '--parse-json',
        action='store_true',
        help='Attempt to parse as JSON and pretty-print'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on parsing errors (with --parse-json)'
    )

    args = parser.parse_args()

    try:
        # Read and parse the file
        content = read_text_file(args.input_file)
        result = parse_text(content, args)

        # Output the result
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Successfully wrote output to {args.output}")
        else:
            print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    parser.add_argument(
        '--remove-numbers',
        action='store_true',
        help='Remove all numeric characters'
    )

    # Add to parse_text():
    if args.remove_numbers:
        import re
        result = re.sub(r'\d+', '', result)