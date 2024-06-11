"""
This script counts the total number of lines in all specified files in specified directories.

Usage:
    python py_line_counter.py <directory1> <directory2> ... [-ext EXTENSIONS]

Example:
    python py_line_counter.py . ./src /path/to/another/directory -ext py frag vert

Args:
    directories (str): One or more paths to directories to search for files.
                       Paths can be relative or absolute.
    -ext, --extensions (str): The file extensions to search for. Default is 'py'.

Output:
    Prints the total number of lines in all specified files in each specified directory.
    Also prints the absolute path of each specified directory.
    If more than one directory is specified, prints the overall total number of lines.
"""

import argparse
import os
import sys

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

EXTENSION_DESCRIPTIONS = {
    "py": "Python",
    "frag": "Fragment Shader",
    "vert": "Vertex Shader",
}


def count_lines_in_files(directory, extensions):
    """
    Counts the total number of lines in all files with the specified extensions in the specified directory.

    Args:
        directory (str): The path to the directory to search for files.
        extensions (list): The file extensions to search for.

    Returns:
        int: The total number of lines in all files with the specified extensions in the directory.
        list: List of tuples containing filenames and their respective line counts.
    """
    total_lines = 0
    processed_files = []
    for filename in os.listdir(directory):
        if any(filename.endswith(f".{ext}") for ext in extensions) and os.path.isfile(
            os.path.join(directory, filename)
        ):
            with open(os.path.join(directory, filename), "r") as file:
                line_count = sum(1 for line in file)
                total_lines += line_count
                processed_files.append((filename, line_count))
    return total_lines, processed_files


def get_extension_description(ext):
    """
    Returns the description for a given file extension.

    Args:
        ext (str): The file extension.

    Returns:
        str: The description for the file extension.
    """
    return EXTENSION_DESCRIPTIONS.get(ext, ext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Counts the total number of lines in all specified files in specified directories."
    )
    parser.add_argument(
        "directories",
        nargs="+",
        help="One or more paths to directories to search for files.",
    )
    parser.add_argument(
        "-ext",
        "--extensions",
        nargs="+",
        default=["py"],
        help="The file extensions to search for. Default is 'py'.",
    )

    args = parser.parse_args()

    overall_total_lines = 0

    for directory in args.directories:
        abs_directory = os.path.abspath(directory)

        if not os.path.isdir(abs_directory):
            print(f"Error: {abs_directory} is not a valid directory.")
            continue

        total_lines, processed_files = count_lines_in_files(
            abs_directory, args.extensions
        )
        overall_total_lines += total_lines
        print(
            f"Total lines in all {', '.join(args.extensions)} files in '{abs_directory}': {total_lines}"
        )
        for filename, line_count in processed_files:
            if filename.endswith(".py"):
                print(f"\t{YELLOW}{line_count:4d} {filename}{RESET}")
            elif filename.endswith(".frag") or filename.endswith(".vert"):
                print(f"\t{BLUE}{line_count:4d} {filename}{RESET}")
            else:
                print(f"\t{line_count:4d} {filename}")

    if len(args.directories) > 1:
        ext_descr_applied_list = list(
            map(lambda ext: EXTENSION_DESCRIPTIONS.get(ext, ext), args.extensions)
        )
        print(
            f"Overall total lines in all {', '.join(ext_descr_applied_list)} files: {overall_total_lines}"
        )
