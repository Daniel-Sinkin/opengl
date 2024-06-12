"""
Note: While this in theory supports windows and linux it's completely untested outside of macOS.
"""

import argparse
import json
import os
import platform
import re


def find_font(font_name_pattern="Arial", system_font_dirs=None) -> dict[str, str]:
    """
    Finds all fonts that match the given regex pattern.

    Parameters:
    font_name_pattern (str): A regex pattern to match font file names.
    system_font_dirs (list of str): List of directories to search for fonts.

    Returns:
    dict: A dictionary where the keys are formatted font names and the values are their paths.

    Example:
    >>> find_font("Arial")
    {
        "Arialhb": "/System/Library/Fonts/ArialHB.ttc",
        "ArialNarrowItalic": "/System/Library/Fonts/Supplemental/Arial Narrow Italic.ttf",
        "ArialBold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ...
    }

    >>> find_font("Bold.*Italic")
    {
        "ArialBoldItalic": "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
        "TimesNewRomanBoldItalic": "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf",
        "TrebuchetMsBoldItalic": "/System/Library/Fonts/Supplemental/Trebuchet MS Bold Italic.ttf",
        ...
    }
    """
    if system_font_dirs is None:
        return {}

    fonts: dict[str, str] = {}
    pattern: re.Pattern[str] = re.compile(font_name_pattern, re.IGNORECASE)

    for font_dir in system_font_dirs:
        for root, dirs, files in os.walk(font_dir):
            for file in files:
                if pattern.search(file):
                    key = file.title().replace(" ", "").split(".")[0]
                    path = os.path.join(root, file)
                    fonts[key] = path

    return fonts


def get_system_font_dirs(os_name):
    """
    Get the default system font directories based on the operating system.

    Parameters:
    os_name (str): The name of the operating system ("windows", "linux", "macos").

    Returns:
    list: A list of directories to search for fonts.
    """
    if os_name == "windows":
        return [
            os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts"),
            "C:/Windows/Fonts",
        ]
    elif os_name == "linux":
        return [
            "/usr/share/fonts",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.fonts"),
            os.path.expanduser("~/.local/share/fonts"),
        ]
    elif os_name == "macos":
        return [
            "/System/Library/Fonts/",
            "/Library/Fonts/",
            os.path.expanduser("~/Library/Fonts/"),
        ]
    else:
        raise ValueError(f"Unsupported operating system: {os_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find fonts on your system using regex patterns."
    )
    parser.add_argument(
        "font_patterns",
        metavar="N",
        type=str,
        nargs="+",
        help="Font regex patterns to search for.",
    )
    parser.add_argument(
        "-os",
        type=str,
        choices=["windows", "linux", "macos"],
        help="Specify the operating system. If not provided, the script will attempt to auto-detect.",
    )
    args = parser.parse_args()

    if args.os:
        os_name = args.os
    else:
        current_os = platform.system().lower()
        if current_os.startswith("darwin"):
            os_name = "macos"
        elif current_os.startswith("win"):
            os_name = "windows"
        elif current_os.startswith("linux"):
            os_name = "linux"
        else:
            raise ValueError(f"Unsupported operating system detected: {current_os}")

    system_font_dirs = get_system_font_dirs(os_name)

    all_fonts = {}
    for pattern in args.font_patterns:
        all_fonts.update(find_font(pattern, system_font_dirs))

    print(json.dumps(all_fonts, indent=4))
