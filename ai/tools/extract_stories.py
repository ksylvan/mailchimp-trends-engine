#!/usr/bin/env python3

"""Story extractor script
This script extracts stories from a markdown file and saves
them to individual files. It uses a specific format for the
markdown content and requires an AUTHOR environment variable to be set.
"""

import sys
import os
import re
import logging
from pathlib import Path
from datetime import datetime
from typing import TextIO, List, Optional

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants for state machine
STATE_LOOKING_FOR_FILENAME = "looking_for_filename"
STATE_LOOKING_FOR_START = "looking_for_start"
STATE_COLLECTING_CONTENT = "collecting_content"

# Compiled regex patterns
FILENAME_PATTERN = re.compile(r"^## Filename: `([^`]+)`$")
START_PATTERN = re.compile(r"^```+markdown\s*$")
END_PATTERN = re.compile(r"^```+\s*$")
IGNORE_PATTERN = re.compile(r"^### Agent Model Used: .*$")


def _write_story_file(
    filename: str,
    content_lines: List[str],
    output_dir: Path,
    current_date: str,
    author: str,
) -> bool:
    """
    Writes the collected story content to a file.

    Args:
        filename: The name of the file to write.
        content_lines: A list of strings representing the content of the story.
        output_dir: The directory where the file should be saved.
        current_date: The current date string to replace {Date} token.
        author: The author string to replace {Author} token.

    Returns:
        True if the file was written successfully, False otherwise.
    """
    output_file = output_dir / filename

    if output_file.exists():
        logging.warning("Output file '%s' already exists. Skipping.", output_file)
        return False

    markdown_content = "".join(content_lines)
    markdown_content = markdown_content.replace("{Date}", current_date)
    markdown_content = markdown_content.replace("{Author}", author)

    try:
        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(markdown_content)
        logging.info("Successfully wrote %s to %s", filename, output_file)
        return True
    except (IOError, PermissionError, OSError) as e:
        logging.error("Failed to write to %s: %s", output_file, e)
        return False


def extract_stories(input_file_path: str) -> int:
    """
    Extract stories from a markdown file and save them to individual files.

    Args:
        input_file_path (str): Path to the input markdown file. Use '-' for stdin.

    Returns:
        int: Number of stories successfully extracted and written.
    """
    load_dotenv()

    author = os.getenv("AUTHOR")
    if not author:
        logging.error("AUTHOR environment variable must be set.")
        return 0

    is_stdin = input_file_path == "-"
    if not is_stdin and not os.path.isfile(input_file_path):
        logging.error("Input file '%s' not found.", input_file_path)
        return 0

    output_dir = Path("./ai")
    output_dir.mkdir(exist_ok=True)

    stories_extracted_count = 0
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_story_filename: Optional[str] = None
    current_story_content_lines: List[str] = []
    current_state: str = STATE_LOOKING_FOR_FILENAME

    try:
        file_source: TextIO = (
            sys.stdin if is_stdin else open(input_file_path, "r", encoding="utf-8")
        )

        with file_source as f_input:
            for line in f_input:
                if IGNORE_PATTERN.match(line):
                    continue
                stripped_line = line.strip()

                if current_state == STATE_LOOKING_FOR_FILENAME:
                    match = FILENAME_PATTERN.match(stripped_line)
                    if match:
                        current_story_filename = match.group(1)
                        current_state = STATE_LOOKING_FOR_START
                        logging.debug("Found filename: %s", current_story_filename)

                elif current_state == STATE_LOOKING_FOR_START:
                    if START_PATTERN.match(line.rstrip()):
                        current_state = STATE_COLLECTING_CONTENT
                        current_story_content_lines = []  # Reset content buffer
                        logging.debug(
                            "Found start marker for %s", current_story_filename
                        )

                elif current_state == STATE_COLLECTING_CONTENT:
                    if END_PATTERN.match(line.rstrip()):
                        if current_story_filename and current_story_content_lines:
                            if _write_story_file(
                                current_story_filename,
                                current_story_content_lines,
                                output_dir,
                                current_date,
                                author,
                            ):
                                stories_extracted_count += 1

                        current_state = STATE_LOOKING_FOR_FILENAME
                        current_story_filename = None
                        current_story_content_lines = []  # Always reset
                    else:
                        current_story_content_lines.append(line)

    except (IOError, PermissionError, UnicodeDecodeError) as e:
        logging.error("Failed to read input: %s", e)
        return 0  # Indicates failure to process input

    if stories_extracted_count == 0:
        logging.warning(
            "No story sections were found or successfully written from the input."
        )

    return stories_extracted_count


def main():
    """Main function to parse command line arguments and run the extraction."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file_path>")
        print("       Use '-' as input_file_path to read from standard input.")
        sys.exit(1)

    input_file_path = sys.argv[1]

    num_extracted = extract_stories(input_file_path)
    if num_extracted > 0:
        source_description = (
            "stdin" if input_file_path == "-" else f"'{input_file_path}'"
        )
        print(
            f"Successfully extracted {num_extracted} stories "
            f"from {source_description} to the ./ai/ directory."
        )
    else:
        print(
            "No stories were extracted or written. Check the log messages above for details."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
