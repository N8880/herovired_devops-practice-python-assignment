"""
Q3: Configuration Management Automation
----------------------------------------
Reads an INI-style configuration file, extracts key-value pairs per
section, stores them in a dictionary, persists that dictionary as JSON
("the database" for this exercise), and prints a human-readable summary.

Usage:
    python config_parser.py [path_to_config_file]

If no path is given, "sample_config.ini" in the same directory is used.
The extracted data is written to "config_data.json", which api.py then
serves via a GET endpoint.
"""

import configparser
import json
import os
import sys


DEFAULT_CONFIG_PATH = "sample_config.ini"
DEFAULT_OUTPUT_PATH = "config_data.json"


def parse_config_file(file_path: str) -> dict:
    """
    Parse an INI-style configuration file into a nested dictionary of
    {section: {key: value}}.

    Raises:
        FileNotFoundError: if the file does not exist.
        configparser.Error: if the file cannot be parsed.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    parser = configparser.ConfigParser()

    try:
        # read() silently ignores missing files, so we already checked above.
        # Any malformed file will raise configparser.Error here.
        with open(file_path, "r") as f:
            parser.read_file(f)
    except configparser.Error as e:
        raise configparser.Error(f"Failed to parse configuration file: {e}")

    return {section: dict(parser.items(section)) for section in parser.sections()}


def save_as_json(data: dict, output_path: str) -> None:
    """Persist the extracted configuration data as a JSON file (our 'database')."""
    try:
        with open(output_path, "w") as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        raise OSError(f"Could not write JSON output to {output_path}: {e}")


def print_summary(data: dict) -> None:
    """Print the parsed configuration in the requested human-readable format."""
    print("Configuration File Parser Results:\n")
    for section, values in data.items():
        print(f"{section}:")
        for key, value in values.items():
            print(f"- {key}: {value}")
        print()


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG_PATH

    try:
        data = parse_config_file(config_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except configparser.Error as e:
        print(f"Error: {e}")
        return

    print_summary(data)

    try:
        save_as_json(data, DEFAULT_OUTPUT_PATH)
        print(f"Saved parsed configuration to '{DEFAULT_OUTPUT_PATH}' (acting as our JSON database).")
        print("Run 'python api.py' and GET http://127.0.0.1:5000/config to fetch this data over HTTP.")
    except OSError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
