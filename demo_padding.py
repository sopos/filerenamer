#!/usr/bin/env python3
"""Demo script showing padding in mathematical operations."""

from src.filerenamer.utils.renamer import apply_pattern


def demo_case(description, filename, search, replace, expected):
    """Run a demo case and print the result."""
    result = apply_pattern(
        filename=filename,
        search=search,
        replace=replace,
        case_sensitive=True,
        use_regex=True
    )
    status = "✓" if result == expected else "✗"
    print(f"{status} {description}")
    print(f"  Input:    {filename}")
    print(f"  Pattern:  {search} → {replace}")
    print(f"  Output:   {result}")
    if result != expected:
        print(f"  Expected: {expected}")
    print()


def main():
    print("=" * 60)
    print("Mathematical Operations with Padding - Demo")
    print("=" * 60)
    print()

    print("Zero-Padding Examples:")
    print("-" * 60)

    demo_case(
        "2-digit zero padding (single digit result)",
        "Episode_5.mp4",
        r'Episode_([0-9]+)\.mp4',
        r'Episode_\{01+2}.mp4',
        "Episode_07.mp4"
    )

    demo_case(
        "2-digit zero padding (double digit result)",
        "Episode_5.mp4",
        r'Episode_([0-9]+)\.mp4',
        r'Episode_\{01+10}.mp4',
        "Episode_15.mp4"
    )

    demo_case(
        "3-digit zero padding",
        "Chapter_7.pdf",
        r'Chapter_([0-9]+)\.pdf',
        r'Chapter_\{001+3}.pdf',
        "Chapter_010.pdf"
    )

    demo_case(
        "4-digit zero padding",
        "Track_5.mp3",
        r'Track_([0-9]+)\.mp3',
        r'Track_\{0001*2}.mp3',
        "Track_0010.mp3"
    )

    demo_case(
        "Overflow (result wider than padding)",
        "S02E99.avi",
        r'S02E([0-9]+)\.avi',
        r'S01E\{01+10}.avi',
        "S01E109.avi"
    )

    print("Space-Padding Examples:")
    print("-" * 60)

    demo_case(
        "2-digit space padding",
        "File_3.txt",
        r'File_([0-9]+)\.txt',
        r'File_\{ 1+2}.txt',
        "File_ 5.txt"
    )

    demo_case(
        "3-digit space padding",
        "Doc_7.md",
        r'Doc_([0-9]+)\.md',
        r'Doc_\{  1+3}.md',
        "Doc_ 10.md"
    )

    print("Complex Examples:")
    print("-" * 60)

    demo_case(
        "Multiple groups with different padding",
        "S2E5.mkv",
        r'S([0-9]+)E([0-9]+)\.mkv',
        r'S\{01-1}E\{02+10}.mkv',
        "S01E15.mkv"
    )

    demo_case(
        "Padding with complex expression",
        "video_3.mp4",
        r'video_([0-9]+)\.mp4',
        r'video_\{001*2+5}.mp4',
        "video_011.mp4"
    )

    demo_case(
        "Padding with subtraction (negative result gets padded)",
        "Chapter_10.pdf",
        r'Chapter_([0-9]+)\.pdf',
        r'Chapter_\{01-15}.pdf',
        "Chapter_-5.pdf"
    )

    print("Backward Compatibility (no padding):")
    print("-" * 60)

    demo_case(
        "Standard math operation without padding",
        "S02E05.avi",
        r'S02E([0-9]+)\.avi',
        r'S01E\{1+10}.avi',
        "S01E15.avi"
    )

    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
