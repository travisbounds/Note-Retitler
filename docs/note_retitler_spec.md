# Note Retitler Script Specification

## Project Overview
The objective is to create a Python script that retitles note files by converting various date formats to a standardized YYYY-MM-DD format.

## Technical Requirements

### Core Functionality
- **Target**: Convert date formats in filenames from MD/MDD/MDYY/MDDYY to YYYY-MM-DD
- **Year Context**: All notes were created in 2025 and should be titled accordingly
- **Date Format Examples**:
  - 2-3 digit: `12` (MD) or `123` (MDD) → `2025-01-02` or `2025-12-03`
  - 4-5 digit: `1225` (MDYY) or `12225` (MDDYY) → `2025-12-25` or `2025-12-22`

### Implementation Guidelines
- **Language**: Python only (minimal external dependencies)
- **Architecture**: Single file, avoid unnecessary abstraction or models
- **CLI Interface**: Use `invoke` for task management and command-line interface
- **Path Handling**: Support both target path flag and current directory operation
- **Code Quality**: Annotate code thoroughly to explain functionality

### Logging and Output
- **Terminal Output**: Print progress during execution
- **Log Files**: Create log file for each run (confirm with user before saving)
- **Error Handling**: Comprehensive error handling and logging throughout

### Documentation
- **README**: Create comprehensive README.md file
- **Code Comments**: Annotate all code to explain functionality

## Development Workflow

### Git Repository Management
- **Repository**: Create private repo at github.com/travisbounds if none exists
- **Initial Setup**: Ensure proper directory structure before repo creation
- **Initial Commit**: Commit only this specification file initially
- **Branching**: Always work in logical branches, never directly in main

### Session Management
- **Session Start Protocol**: Always review these files at session start:
  1. `note_retitler_spec.md` (this file)
  2. `release_notes.md` (project progress tracking)
  3. `memory.md` (working notes and session continuity)
- **Documentation Updates**: Record all work in release_notes.md
- **Memory Tracking**: Capture thoughts, concerns, progress, and open tasks in memory.md

### Communication Guidelines
- **Tone**: Direct and professional, avoid sycophantic responses
- **Documentation**: Never remove content from this specification
- **Improvements**: Review and enhance this document while preserving all requirements

## Agent Directives and Learned Behaviors
*This section will be populated with insights and principles discovered during development*