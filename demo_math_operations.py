"""Demo script showing mathematical operations in regex replacements."""

from src.filerenamer.utils.renamer import apply_pattern


def demo():
    print("=" * 60)
    print("Mathematical Operations in Regex Replacements Demo")
    print("=" * 60)

    examples = [
        {
            "filename": "S02E01",
            "search": r'S02E([0-9]+)',
            "replace": r'S01E\{1+10}',
            "description": "Add 10 to episode number"
        },
        {
            "filename": "S05E20.mkv",
            "search": r'S05E([0-9]+)',
            "replace": r'S04E\{1-10}',
            "description": "Subtract 10 from episode number"
        },
        {
            "filename": "Chapter_5.pdf",
            "search": r'Chapter_([0-9]+)',
            "replace": r'Chapter_\{1*2}',
            "description": "Double the chapter number"
        },
        {
            "filename": "video_3.mp4",
            "search": r'video_([0-9]+)',
            "replace": r'video_\{1*2+5}',
            "description": "Complex expression: multiply by 2 and add 5"
        },
        {
            "filename": "S02E05.avi",
            "search": r'S([0-9]+)E([0-9]+)',
            "replace": r'S\{1-1}E\{2+10}',
            "description": "Multiple groups: decrement season, add 10 to episode"
        },
        {
            "filename": "Track_10_of_20.mp3",
            "search": r'Track_([0-9]+)_of_([0-9]+)',
            "replace": r'Track_\{1+5}_of_\{2}',
            "description": "Add 5 to first number, keep second unchanged"
        }
    ]

    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   Original:    {example['filename']}")
        print(f"   Pattern:     {example['search']}")
        print(f"   Replace:     {example['replace']}")

        result = apply_pattern(
            example['filename'],
            example['search'],
            example['replace'],
            case_sensitive=True,
            use_regex=True
        )

        print(f"   Result:      {result}")

    print("\n" + "=" * 60)
    print("\nSyntax: Use \\{N+expr} where N is the capture group number")
    print("Supported operations: +, -, *, /, //, %, **")
    print("Examples: \\{1+10}, \\{2*2}, \\{1//2}, \\{1**2}")
    print("=" * 60)


if __name__ == "__main__":
    demo()
