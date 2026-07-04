"""
Q4: Directory Backup Utility
-----------------------------
Copies all files from a source directory to a destination directory.
If a file with the same name already exists at the destination, a
timestamp is appended to the copied file's name to keep it unique
rather than overwriting the existing backup.

Usage:
    python backup.py /path/to/source /path/to/destination
"""

import os
import shutil
import sys
from datetime import datetime


def make_unique_destination_path(destination_dir: str, filename: str) -> str:
    """
    Given a destination directory and a filename, return a path that does
    not collide with an existing file. If 'report.txt' already exists,
    the new path becomes something like 'report_20260704_153012.txt'.
    """
    candidate_path = os.path.join(destination_dir, filename)

    if not os.path.exists(candidate_path):
        return candidate_path

    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{name}_{timestamp}{ext}"
    new_path = os.path.join(destination_dir, new_filename)

    # Extremely unlikely, but guard against a same-second collision too.
    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{name}_{timestamp}_{counter}{ext}"
        new_path = os.path.join(destination_dir, new_filename)
        counter += 1

    return new_path


def backup_directory(source_dir: str, destination_dir: str) -> None:
    """
    Copy every file (non-recursively) from source_dir into destination_dir,
    renaming with a timestamp on collisions. Raises informative exceptions
    on invalid directories.
    """
    if not os.path.isdir(source_dir):
        raise NotADirectoryError(f"Source directory does not exist: {source_dir}")

    if not os.path.isdir(destination_dir):
        raise NotADirectoryError(f"Destination directory does not exist: {destination_dir}")

    copied, skipped = 0, 0

    for entry in os.listdir(source_dir):
        source_path = os.path.join(source_dir, entry)

        if not os.path.isfile(source_path):
            # Skip subdirectories; this script backs up files only.
            continue

        try:
            dest_path = make_unique_destination_path(destination_dir, entry)
            shutil.copy2(source_path, dest_path)
            print(f"Copied: {entry} -> {os.path.basename(dest_path)}")
            copied += 1
        except (OSError, shutil.Error) as e:
            print(f"Warning: could not copy '{entry}': {e}")
            skipped += 1

    print(f"\nBackup complete. Files copied: {copied}, files skipped due to errors: {skipped}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python backup.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_dir, destination_dir = sys.argv[1], sys.argv[2]

    try:
        backup_directory(source_dir, destination_dir)
    except NotADirectoryError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during backup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
