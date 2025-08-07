# Note Retitler

A Python script that standardizes date formats in note filenames by converting various date patterns to YYYY-MM-DD format.

## Overview

This tool processes note files and renames them by converting date formats from:
- **MD/MDD** (2-3 digits): `12`, `123` → `2025-01-02`, `2025-12-03`
- **MDYY/MDDYY** (4-5 digits): `1225`, `12225` → `2025-12-25`, `2025-12-22`

All dates are assumed to be from **2025**.

## Installation

### Option 1: One-Click Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd note_retitler_spec

# Run the one-click installer
./install.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the tool for immediate use

### Option 2: Manual Installation

#### With Virtual Environment (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd note_retitler_spec

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and the package
pip install -r requirements.txt
pip install -e .
```

#### System-wide Installation

```bash
# After cloning the repository
cd note_retitler_spec
sudo pip install -e .
```

**Note:** System-wide installation allows you to use `retitle` command from anywhere without activating a virtual environment.

## Usage

### Method 1: Using the `retitle` Command (After Installation)

```bash
# Activate virtual environment (if using venv)
source venv/bin/activate

# Process current directory with confirmation prompts
retitle

# Process specific directory
retitle /path/to/notes

# Skip all confirmations (auto-yes to all prompts)
retitle --yes
retitle -y

# Force mode (same as --yes)
retitle --force
retitle -f

# Save log file automatically
retitle --log

# Combine options
retitle /path/to/notes --yes --log
```

### Method 2: Using Invoke Tasks (Development)

```bash
# Activate virtual environment
source venv/bin/activate

# Process current directory
invoke retitle

# Process specific directory
invoke retitle --path /path/to/notes

# Skip confirmations
invoke retitle --yes

# Force log file creation
invoke retitle --log

# Run tests
invoke test

# Show format help
invoke help-formats
```

### Method 3: Direct Python Execution

```bash
# Activate virtual environment
source venv/bin/activate

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
| MDD | `123` | `2025-01-23` | Month 1, Day 23 |
| **M/DD** | `714` | `2025-07-14` | **Month 7, Day 14 (from 7/14 with slashes stripped)** |
| MMD | `123` | `2025-12-03` | Month 12, Day 3 |
| MDYY | `1225` | `2025-01-02` | Month 1, Day 2, Year 25 |
| MMDD | `1231` | `2025-12-31` | Month 12, Day 31 |
| MDDYY | `12225` | `2025-12-22` | Month 12, Day 22, Year 25 |

**Special Handling:**
- **Pure numeric filenames** (like `714.txt`) are prioritized for M/DD parsing
- Files with names like `714.txt` from `7/14` dates are the **primary target**

### Output Format

All dates are converted to **YYYY-MM-DD** format (ISO 8601 standard).

## Features

- **Path Confirmation**: Shows target directory and file count before processing
- **Force Mode**: Skip all confirmations with `--yes` or `--force` flags
- **Comprehensive Logging**: Creates detailed log files with timestamps
- **Progress Tracking**: Real-time progress output to terminal
- **Error Handling**: Robust error handling for file operations
- **Safety Checks**: Prevents overwriting existing files
- **Flexible Input**: Works with current directory or specified path
- **Pure Numeric Support**: Handles files with only numeric names (primary target: 7/14 → 714)
- **Test Persistence**: Automatically saves test results to log files
- **Multiple Installation Options**: Virtual environment, system-wide, or one-click install

## Examples

### Before and After

```
Original filenames (primary targets):
- 714.txt                    # From 7/14 with slashes stripped
- meeting_714.docx           # From 7/14 format
- 825.md                     # From 8/25 format
- project_1225.md            # Standard MMDD format
- summary_12225.docx         # MMDYY format

After processing:
- 2025-07-14.txt
- meeting_2025-07-14.docx
- 2025-08-25.md
- project_2025-12-25.md
- summary_2025-12-22.docx
```

### Sample Output

```bash
$ retitle /path/to/notes
Target directory: /path/to/notes
Found 5 files to process
Proceed with processing 5 files in '/path/to/notes'? (y/n): y
Save log file as 'note_retitler_20250807_142530.log'? (y/n): y

2025-08-07 14:25:30 - INFO - Starting Note Retitler Script
2025-08-07 14:25:30 - INFO - Found 5 files to process
2025-08-07 14:25:30 - INFO - Renamed: 714.txt -> 2025-07-14.txt
2025-08-07 14:25:30 - INFO - Renamed: meeting_825.docx -> meeting_2025-08-25.docx

Processing complete. Renamed 2 files.
Log saved to: note_retitler_20250807_142530.log
```

```bash
$ retitle --yes --log
Target directory: /home/user/notes
Found 3 files to process
Log file will be saved as: note_retitler_20250807_142530.log

2025-08-07 14:25:30 - INFO - Starting Note Retitler Script
2025-08-07 14:25:30 - INFO - Found 3 files to process
2025-08-07 14:25:30 - INFO - Renamed: 714.txt -> 2025-07-14.txt

Processing complete. Renamed 1 files.
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