# File Organizer

File Organizer is a simple command-line utility that organizes files in a directory by their extensions.

## Installation

No external dependencies are required. Python 3 is needed.

## Usage

Run the tool with the organize command and a target directory.

python main.py organize /path/to/directory [--dry-run]

The --dry-run option shows what would be moved without actually moving files.

## Example

Run this command to organize a directory.

python main.py organize ./notes

The tool moves all files in ./notes into subfolders named after their extensions, such as jpg, pdf, txt, or others.

## License

MIT License.
