"""
Invoke tasks for Note Retitler Script - Root Level

This module provides the root-level invoke tasks that import from the src package.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import all tasks from the src package
from src.tasks import *