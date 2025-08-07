#!/usr/bin/env python3
"""
Note Retitler - Main Entry Point

This is the main entry point for the note retitler script.
It imports and runs the functionality from the src package.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.note_retitler import main

if __name__ == "__main__":
    main()