"""Entry point for the File Renamer application."""

import sys
from pathlib import Path

from .app import FileRenamerApp


def main():
    """Run the File Renamer application."""
    # Get starting directory from command line args, default to current directory
    if len(sys.argv) > 1:
        start_path = Path(sys.argv[1]).resolve()
        if not start_path.exists() or not start_path.is_dir():
            print(f"Error: '{start_path}' is not a valid directory", file=sys.stderr)
            sys.exit(1)
    else:
        start_path = Path.cwd()

    app = FileRenamerApp(start_path=start_path)
    app.run()


if __name__ == "__main__":
    main()
