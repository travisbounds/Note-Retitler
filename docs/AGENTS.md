# Agent Guidelines for Note Retitler Project

## Session Start Protocol
- **ALWAYS** review note_retitler_spec.md, release_notes.md, and memory.md at session start
- Follow ALL instructions in the spec file without stopping unless you have questions
- Update memory.md with working thoughts, concerns, and progress throughout session

## Build/Test/Lint Commands
- **Run script**: `python3 note_retitler.py [--path PATH]`
- **Test**: `python3 -m pytest` (if tests exist)
- **Lint**: `python3 -m ruff check .` or `python3 -m flake8 .`
- **Format**: `python3 -m black .`

## Code Style Guidelines
- **Language**: Python 3.12+ only
- **Libraries**: Use minimal dependencies, prefer standard library
- **Imports**: Standard library first, then third-party, then local imports
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Types**: Use type hints for function parameters and return values
- **Error Handling**: Include comprehensive error handling and logging
- **Comments**: Annotate code to explain functionality (required per spec)

## Project Requirements
- Use `invoke` for CLI interface and task management
- Create log files for each run (confirm with user before saving)
- Print progress to terminal during execution
- Target date format conversion: MD/MDD/MDYY/MDDYY → YYYY-MM-DD (2025)
- Work in logical branches, never in main
- Update release_notes.md and memory.md for all work
- Always review note_retitler_spec.md, release_notes.md, and memory.md at session start