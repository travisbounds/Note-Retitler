"""
Note Retitler Package

A Python package for standardizing date formats in note filenames.
"""

from .note_retitler import parse_date_from_filename, generate_new_filename, process_directory, setup_logging

__version__ = "1.0.0"
__author__ = "Travis Bounds"

__all__ = [
    "parse_date_from_filename",
    "generate_new_filename", 
    "process_directory",
    "setup_logging"
]