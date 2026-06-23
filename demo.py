#!/usr/bin/env python3
"""
Demo script showing the File Renamer in action.
This creates a simple demo with sample data.
"""

from pathlib import Path
from filerenamer.app import FileRenamerApp

def main():
    """Run the File Renamer demo."""
    # Use test_files directory if it exists, otherwise current directory
    test_path = Path("test_files")
    if not test_path.exists():
        test_path = Path.cwd()

    print(f"Starting File Renamer in: {test_path}")
    print("\nInstructions:")
    print("1. Type a search pattern in the Search field (try 'file')")
    print("2. Type a replacement in the Replace field (try 'doc')")
    print("3. Watch the preview update in real-time!")
    print("4. Use Space to toggle file selection")
    print("5. Use Enter to edit individual filenames")
    print("6. Click Apply to rename, or Exit to quit")
    print("\nStarting application...\n")

    app = FileRenamerApp(start_path=test_path)
    app.run()

if __name__ == "__main__":
    main()
