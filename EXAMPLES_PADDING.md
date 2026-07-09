# Padding Examples - File Renamer

This document contains practical examples of using number padding with mathematical operations.

## Table of Contents
- [Basic Zero-Padding](#basic-zero-padding)
- [Basic Space-Padding](#basic-space-padding)
- [Episode/Season Numbering](#episodeseason-numbering)
- [Chapter/Track Numbering](#chaptertrack-numbering)
- [Complex Scenarios](#complex-scenarios)

## Basic Zero-Padding

### 2-Digit Zero-Padding

Useful for keeping file lists sorted numerically:

```
Files:           Pattern:                        Result:
Episode_1.mp4    Episode_([0-9]+)   →           Episode_01.mp4
Episode_5.mp4    Episode_\{01+0}                Episode_05.mp4
Episode_12.mp4                                  Episode_12.mp4
```

With arithmetic:

```
Files:           Pattern:                        Result:
Episode_1.mp4    Episode_([0-9]+)   →           Episode_06.mp4
Episode_5.mp4    Episode_\{01+5}                Episode_10.mp4
Episode_12.mp4                                  Episode_17.mp4
```

### 3-Digit Zero-Padding

For larger series:

```
Files:            Pattern:                       Result:
Chapter_1.pdf     Chapter_([0-9]+)   →          Chapter_001.pdf
Chapter_15.pdf    Chapter_\{001+0}              Chapter_015.pdf
Chapter_100.pdf                                 Chapter_100.pdf
```

### 4-Digit Zero-Padding

For very large collections:

```
Files:            Pattern:                       Result:
Track_1.mp3       Track_([0-9]+)     →          Track_0001.mp3
Track_50.mp3      Track_\{0001+0}               Track_0050.mp3
Track_999.mp3                                   Track_0999.mp3
```

## Basic Space-Padding

### 2-Digit Space-Padding

For tabular displays:

```
Files:           Pattern:                        Result:
File_1.txt       File_([0-9]+)      →           File_ 1.txt
File_5.txt       File_\{ 1+0}                   File_ 5.txt
File_12.txt                                     File_12.txt
```

### 3-Digit Space-Padding

```
Files:           Pattern:                        Result:
Doc_3.md         Doc_([0-9]+)       →           Doc_  3.md
Doc_25.md        Doc_\{  1+0}                   Doc_ 25.md
Doc_100.md                                      Doc_100.md
```

## Episode/Season Numbering

### TV Show Renaming with Padding

Convert between different episode numbering schemes:

```
Files:                Pattern:                           Result:
S02E01.mkv            S02E([0-9]+)        →             S01E11.mkv
S02E05.mkv            S01E\{01+10}                      S01E15.mkv
S02E10.mkv                                              S01E20.mkv
```

### Multi-Season Conversion

```
Files:                Pattern:                           Result:
S2E5.avi              S([0-9]+)E([0-9]+)  →             S01E15.avi
S3E12.avi             S\{01-1}E\{02+10}                 S02E22.avi
S5E8.avi                                                S04E18.avi
```

Explanation:
- `S\{01-1}` - Subtract 1 from season, zero-pad to 2 digits
- `E\{02+10}` - Add 10 to episode, zero-pad to 2 digits

### Continuous Episode Numbering

Convert S##E## format to continuous numbering:

```
Files:                Pattern:                           Result:
S01E01.mp4            S([0-9]+)E([0-9]+)  →             Episode_001.mp4
S01E12.mp4            Episode_\{002+(1-1)*24}           Episode_012.mp4
S02E05.mp4                                              Episode_029.mp4
```

Formula: `(season-1) × 24 + episode` assumes 24 episodes per season

## Chapter/Track Numbering

### Sequential Chapter Renaming

Renumber chapters sequentially with padding:

```
Files:                  Pattern:                         Result:
Chapter_5.pdf           Chapter_([0-9]+)     →          Chapter_001.pdf
Chapter_8.pdf           Chapter_\{001+(1-5)+1}          Chapter_005.pdf
Chapter_12.pdf                                          Chapter_009.pdf
```

Formula: `(current - 5) + 1` to start from 1

### Track Numbering with Offset

Add padding to existing track numbers:

```
Files:                  Pattern:                         Result:
Track_1_song.mp3        Track_([0-9]+)       →          Track_01_song.mp3
Track_5_song.mp3        Track_\{01+0}                   Track_05_song.mp3
Track_12_song.mp3                                       Track_12_song.mp3
```

### Disc/Track Combined Numbering

```
Files:                  Pattern:                         Result:
Disc1_Track03.flac      Disc([0-9]+)_Track([0-9]+) →    Track_103.flac
Disc2_Track07.flac      Track_\{1}0\{2+0}               Track_207.flac
Disc3_Track12.flac                                      Track_312.flac
```

Pattern creates format: `[disc][track with padding]`

## Complex Scenarios

### Date-Based Renaming with Padding

```
Files:                  Pattern:                         Result:
2024-1-5_report.pdf     20([0-9]+)-([0-9]+)-([0-9]+) →  2024_01_05_report.pdf
2024-12-25_data.csv     20\1_\{02+0}_\{03+0}            2024_12_25_data.csv
```

### Version Number Incrementing

```
Files:                  Pattern:                         Result:
app_v1.2.tar.gz         app_v([0-9]+)\.([0-9]+) →       app_v01.03.tar.gz
lib_v2.15.zip           \w+_v\{01+0}.\{02+1}            lib_v02.16.zip
```

Increment minor version, add padding to both major and minor

### Photo Series with Gap Filling

Insert photos into a sequence:

```
Original sequence:           After inserting 3 photos at position 5:
Photo_001.jpg                Photo_001.jpg
Photo_002.jpg                Photo_002.jpg
Photo_003.jpg                Photo_003.jpg
Photo_004.jpg                Photo_004.jpg
Photo_005.jpg    →           Photo_008.jpg
Photo_006.jpg    Pattern:    Photo_009.jpg
Photo_007.jpg    Photo_([0-9]+)  where ([0-9]+) >= 5
                 Photo_\{001+3}

Then insert new photos as Photo_005, Photo_006, Photo_007
```

### Course Material Organization

```
Files:                     Pattern:                            Result:
Lecture_2_Intro.mp4        Lecture_([0-9]+)        →          Lecture_02_Intro.mp4
Lecture_5_Advanced.mp4     Lecture_\{02+0}                    Lecture_05_Advanced.mp4
Lecture_12_Final.mp4                                          Lecture_12_Final.mp4
```

### Multi-Capture with Different Padding

```
Files:                     Pattern:                            Result:
Y2024M1D5.log             Y([0-9]+)M([0-9]+)D([0-9]+)  →     2024-01-05.log
Y2024M12D25.log           \{1+0}-\{02+0}-\{03+0}             2024-12-25.log
```

- Year: No padding (4 digits already)
- Month: Zero-pad to 2 digits
- Day: Zero-pad to 2 digits

## Tips and Tricks

### When to Use Zero-Padding

Use zero-padding when:
- Files need to sort correctly in file managers (01, 02, ... 10, 11)
- You have more than 9 items in a sequence
- Consistency in digit count is important

### When to Use Space-Padding

Use space-padding when:
- Creating fixed-width text output
- Aligning numbers in terminal displays
- Preparing data for tabular formats

### Overflow Behavior

When the result is wider than the padding:

```
Search:   Episode_([0-9]+)
Replace:  Episode_\{01+100}
Input:    Episode_5.mp4
Output:   Episode_105.mp4     (3 digits, padding ignored)
```

The padding is a minimum width, not a truncation.

### Negative Numbers

Padding respects negative signs:

```
Search:   Value_([0-9]+)
Replace:  Value_\{01-10}
Input:    Value_5.txt
Output:   Value_-5.txt        (padding after the minus)
```

### Combining with Standard Backreferences

You can mix padded math operations with standard backreferences:

```
Search:   S([0-9]+)E([0-9]+)_(\w+)
Replace:  S\{01-1}E\{02+10}_\3
Input:    S2E5_episode_title.avi
Output:   S01E15_episode_title.avi
```

- Groups 1 and 2: Use math with padding
- Group 3: Standard backreference (no modification)

## Quick Reference

| Padding Format | Example  | Input | Output | Description              |
|----------------|----------|-------|--------|--------------------------|
| `\{01+N}`      | `\{01+5}`| 3     | 08     | 2-digit zero-padding     |
| `\{001+N}`     | `\{001+5}`| 3    | 008    | 3-digit zero-padding     |
| `\{0001+N}`    | `\{0001+5}`| 3   | 0008   | 4-digit zero-padding     |
| `\{ 1+N}`      | `\{ 1+5}`| 3     | ` 8`   | 2-digit space-padding    |
| `\{  1+N}`     | `\{  1+5}`| 3    | ` 8`   | 3-digit space-padding    |
| `\{1+N}`       | `\{1+5}` | 3     | 8      | No padding               |

## See Also

- [MATH_OPERATIONS.md](MATH_OPERATIONS.md) - Complete reference for mathematical operations
- [USAGE.md](USAGE.md) - General usage guide
- [README.md](README.md) - Project overview
