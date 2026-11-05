#!/usr/bin/env python3
"""
File Organizer - a command-line tool to sort files into subfolders based on extension.
"""

import argparse
import shutil
from pathlib import Path


def organize_files(root_path: Path, dry_run: bool = False) -> None:
    """
    Move files in root_path into subfolders named after their extension.
    Files without an extension go to 'others'.
    If dry_run is True, only prints the actions without moving files.
    """
    for entry in root_path.iterdir():
        if entry.is_file():
            ext = entry.suffix.lower().lstrip('.') or 'others'
            target_dir = root_path / ext
            target_path = target_dir / entry.name

            if dry_run:
                print(f"Would move {entry} to {target_path}")
            else:
                target_dir.mkdir(exist_ok=True)
                if entry != target_path:
                    shutil.move(str(entry), str(target_path))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Organize files into subfolders by extension.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    organize_parser = subparsers.add_parser('organize', help='Organize files in a directory')
    organize_parser.add_argument('directory', type=Path, help='Path to the directory to organize')
    organize_parser.add_argument('--dry-run', action='store_true', help='Show actions without moving files')

    return parser.parse_args(argv)


def main():
    args = parse_args()
    if args.command == 'organize':
        organize_files(args.directory, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
