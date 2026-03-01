"""Tests for the text file parsing module."""

import tempfile
import os
import argparse
from pathlib import Path
from agentsecops.parsing.textfile import read_text_file, parse_text


def test_read_text_file_with_valid_file():
    """Test reading a valid text file."""
    test_content = "Hello, World!\nThis is a test file."

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        # Test reading the file
        content = read_text_file(temp_file_path)
        assert content == test_content
    finally:
        os.unlink(temp_file_path)


def test_read_text_file_with_encoding_issue():
    """Test reading a file with encoding issues."""
    # Create a file with latin-1 encoding
    test_content = "Hello, World!\nCafé au lait."

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, encoding="latin-1", suffix=".txt"
    ) as temp_file:
        temp_file.write(test_content)
        temp_file_path = temp_file.name

    try:
        # Test reading the file (should handle encoding issues)
        content = read_text_file(temp_file_path)
        assert "Café" in content
    finally:
        os.unlink(temp_file_path)


def test_read_text_file_nonexistent():
    """Test reading a non-existent file."""
    try:
        content = read_text_file("/nonexistent/file.txt")
        assert False, "Should have raised an exception"
    except (FileNotFoundError, ValueError):
        # Expected exception
        pass


def test_read_text_file_from_stdin():
    """Test reading from stdin when no file path is provided."""
    import sys
    from io import StringIO

    # Save original stdin
    original_stdin = sys.stdin

    try:
        # Set up mock stdin
        test_content = "Hello from stdin"
        sys.stdin = StringIO(test_content)

        # Test reading from stdin
        content = read_text_file(None)
        assert content == test_content
    finally:
        # Restore original stdin
        sys.stdin = original_stdin


def test_parse_text_lowercase():
    """Test lowercase transformation."""
    content = "HELLO WORLD"
    args = argparse.Namespace(lowercase=True)

    result = parse_text(content, args)
    assert result == "hello world"


def test_parse_text_strip():
    """Test strip transformation."""
    content = "  Hello World  "
    args = argparse.Namespace(strip=True)

    result = parse_text(content, args)
    assert result == "Hello World"


def test_parse_text_remove_whitespace():
    """Test remove whitespace transformation."""
    content = "Hello    World   with  extra  spaces"
    args = argparse.Namespace(remove_whitespace=True)

    result = parse_text(content, args)
    assert result == "Hello World with extra spaces"


def test_parse_text_lines():
    """Test line-by-line processing."""
    content = "Line 1\n\nLine 2\n  Line 3  \n"
    args = argparse.Namespace(lines=True)

    result = parse_text(content, args)
    expected = "Line 1\nLine 2\nLine 3"
    assert result == expected


def test_parse_text_json():
    """Test JSON parsing."""
    content = '{"name": "John", "age": 30}'
    args = argparse.Namespace(parse_json=True)

    result = parse_text(content, args)
    # Should be pretty-printed JSON
    assert "{\n  " in result
    assert '"name": "John"' in result


def test_parse_text_invalid_json():
    """Test invalid JSON handling."""
    content = "Not a JSON string"
    args = argparse.Namespace(parse_json=True, strict=False)

    result = parse_text(content, args)
    # Should return original content when not strict
    assert result == content


def test_parse_text_invalid_json_strict():
    """Test invalid JSON handling in strict mode."""
    content = "Not a JSON string"
    args = argparse.Namespace(parse_json=True, strict=True)

    try:
        result = parse_text(content, args)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Invalid JSON format" in str(e)


def test_parse_text_no_args():
    """Test parsing with no arguments."""
    content = "Hello, World!"
    args = argparse.Namespace()

    result = parse_text(content, args)
    assert result == content


def test_parse_text_combined_options():
    """Test multiple parsing options combined."""
    content = "  HELLO   WORLD  \n\n  "
    args = argparse.Namespace(lowercase=True, strip=True, remove_whitespace=True)

    result = parse_text(content, args)
    expected = "hello world"
    assert result == expected


def test_read_text_file_with_path_object():
    """Test reading a file using Path object."""
    test_content = "Hello from Path object"

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_file.write(test_content)
        temp_file_path = Path(temp_file.name)

    try:
        # Test reading with Path object
        content = read_text_file(temp_file_path)
        assert content == test_content
    finally:
        os.unlink(temp_file_path)


if __name__ == "__main__":
    test_read_text_file_with_valid_file()
    test_read_text_file_with_encoding_issue()
    test_read_text_file_nonexistent()
    test_read_text_file_from_stdin()
    test_parse_text_lowercase()
    test_parse_text_strip()
    test_parse_text_remove_whitespace()
    test_parse_text_lines()
    test_parse_text_json()
    test_parse_text_invalid_json()
    test_parse_text_invalid_json_strict()
    test_parse_text_no_args()
    test_parse_text_combined_options()
    test_read_text_file_with_path_object()
    print("All textfile parsing tests passed!")
