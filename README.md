# Note Retitler

A Python script that standardizes date formats in note filenames by converting various date patterns to YYYY-MM-DD format.

## Overview

This tool processes note files and renames them by converting date formats from:
- **MD/MDD** (2-3 digits): `12`, `123` → `2025-01-02`, `2025-12-03`
- **MDYY/MDDYY** (4-5 digits): `1225`, `12225` → `2025-12-25`, `2025-12-22`

All dates are assumed to be from **2025**.

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface (Invoke)

The script uses `invoke` for task management and CLI interface:

```bash
# Process current directory
invoke retitle

# Process specific directory
invoke retitle --path /path/to/notes

# Force log file creation
invoke retitle --log

# Run tests
invoke test

# Show format help
invoke help-formats
```

### Direct Python Execution

You can also run the script directly:

```bash
# Process current directory
python3 note_retitler.py

# Process specific directory
python3 note_retitler.py /path/to/notes
```

## Supported Date Formats

### Input Formats

| Format | Example | Converts To | Description |
|--------|---------|-------------|-------------|
| MD | `12` | `2025-01-02` | Month 1, Day 2 |
| MDD | `123` | `2025-12-03` | Month 12, Day 3 |
| MDYY | `1225` | `2025-01-02` | Month 1, Day 2, Year 25 |
| MMDD | `1231` | `2025-12-31` | Month 12, Day 31 |
| MDDYY | `12225` | `2025-12-22` | Month 12, Day 22, Year 25 |

### Output Format

All dates are converted to **YYYY-MM-DD** format (ISO 8601 standard).

## Features

- **Comprehensive Logging**: Creates detailed log files with timestamps
- **Progress Tracking**: Real-time progress output to terminal
- **Error Handling**: Robust error handling for file operations
- **Safety Checks**: Prevents overwriting existing files
- **Flexible Input**: Works with current directory or specified path
- **User Confirmation**: Asks before creating log files

## Examples

### Before and After

```
Original filenames:
- meeting_notes_123.txt
- project_1225.md
- summary_12225.docx

After processing:
- meeting_notes_2025-12-03.txt
- project_2025-12-25.md
- summary_2025-12-22.docx
```

### Sample Output

```bash
$ invoke retitle
Save log file as 'note_retitler_20250807_142530.log'? (y/n): y
Processing directory: /home/user/notes

2025-08-07 14:25:30 - INFO - Starting Note Retitler Script
2025-08-07 14:25:30 - INFO - Found 5 files to process
2025-08-07 14:25:30 - INFO - Renamed: notes_123.txt -> notes_2025-12-03.txt
2025-08-07 14:25:30 - INFO - Renamed: meeting_1225.md -> meeting_2025-12-25.md

Processing complete. Renamed 2 files.
Log saved to: note_retitler_20250807_142530.log
```

## Testing

Run the built-in tests to verify functionality:

```bash
invoke test
```

This will test various date format parsing scenarios and report results.

## Requirements

- Python 3.12+
- invoke 2.0.0+

## Project Structure

```
note_retitler_spec/
├── src/                     # Source code
│   ├── __init__.py         # Package initialization
│   ├── note_retitler.py    # Core functionality
│   └── tasks.py            # Invoke task definitions
├── docs/                   # Documentation
│   ├── AGENTS.md           # Guidelines for AI agents
│   ├── note_retitler_spec.md # Project specification
│   ├── release_notes.md    # Development progress
│   └── memory.md           # Session working notes
├── examples/               # Example files and tests
│   └── test_files/         # Sample files for testing
├── tests/                  # Test files (future)
├── note_retitler.py        # Main entry point
├── tasks.py                # Root-level invoke tasks
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development

This project follows specific development guidelines:

- Work in logical branches, never directly in `main`
- Update `release_notes.md` for all changes
- Use `memory.md` for session continuity
- Follow Python best practices with type hints and comprehensive error handling

## License

This project is for personal use. See project specification for details.