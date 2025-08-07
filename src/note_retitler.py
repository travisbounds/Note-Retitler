#!/usr/bin/env python3
"""
Note Retitler Script

This script converts date formats in note filenames from various formats
(MD, MDD, MDYY, MDDYY) to standardized YYYY-MM-DD format.

All dates are assumed to be from 2025.
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime


def setup_logging(log_file: str) -> logging.Logger:
    """
    Configure logging to both file and console.
    
    Args:
        log_file: Path to the log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('note_retitler')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def _parse_numeric_date(date_str: str) -> Optional[Tuple[str, str]]:
    """
    Helper function to parse a numeric date string.
    
    Args:
        date_str: Numeric string to parse as date
        
    Returns:
        Tuple of (original_date_part, formatted_date) or None if invalid
    """
    try:
        if len(date_str) == 2:
            # MD format: single digit month, single digit day
            month = int(date_str[0])
            day = int(date_str[1])
            if 1 <= month <= 9 and 1 <= day <= 9:
                return date_str, f"2025-0{month}-0{day}"
                
        elif len(date_str) == 3:
            # Special handling for 7/14 format (714)
            # Try M/DD format first: 714 -> 7/14 -> 2025-07-14
            month = int(date_str[0])
            day = int(date_str[1:])
            if 1 <= month <= 9 and 1 <= day <= 31:
                return date_str, f"2025-0{month}-{day:02d}"
            
            # MDD format: single digit month, double digit day
            # Based on spec example: 123 -> 2025-12-03 (month 12, day 3)
            # This suggests MMD interpretation: first two digits = month, last digit = day
            month = int(date_str[:2])
            day = int(date_str[2])
            if 1 <= month <= 12 and 1 <= day <= 9:
                return date_str, f"2025-{month:02d}-0{day}"
                
        elif len(date_str) == 4:
            # MMDD format: two digit month, two digit day
            # Based on spec example: 1225 -> 2025-12-25
            month = int(date_str[:2])
            day = int(date_str[2:])
            if 1 <= month <= 12 and 1 <= day <= 31:
                return date_str, f"2025-{month:02d}-{day:02d}"
            
            # Check if it ends with 25 (year 2025) - MDYY format
            if date_str.endswith('25'):
                # MDYY: single digit month, single digit day, year 25
                month = int(date_str[0])
                day = int(date_str[1])
                if 1 <= month <= 9 and 1 <= day <= 9:
                    return date_str, f"2025-0{month}-0{day}"
                
        elif len(date_str) == 5:
            # Must end with 25 for year 2025
            if date_str.endswith('25'):
                # Based on spec example: 12225 -> 2025-12-22
                # This is MMDYY: first two digits = month, next two digits = day, last two = year
                month = int(date_str[:2])
                day = int(date_str[2:4])  # Take two digits for day
                if 1 <= month <= 12 and 1 <= day <= 31:
                    return date_str, f"2025-{month:02d}-{day:02d}"
                
                # Alternative: MDDYY (month 1-9, day 10-31, year 25)
                month = int(date_str[0])
                day = int(date_str[1:3])
                if 1 <= month <= 9 and 1 <= day <= 31:
                    return date_str, f"2025-0{month}-{day:02d}"
                    
    except ValueError:
        # Invalid date components
        pass
    
    return None


def parse_date_from_filename(filename: str) -> Optional[Tuple[str, str]]:
    """
    Extract and parse date from filename, converting to YYYY-MM-DD format.
    
    Handles these formats based on spec:
    - MD (2-3 digits): 12 -> 2025-01-02, 123 -> 2025-12-03  
    - MDYY/MDDYY (4-5 digits): 1225 -> 2025-12-25, 12225 -> 2025-12-22
    - Files with only numeric names (like "714" from "7/14" with slashes stripped)
    
    Args:
        filename: The filename to parse
        
    Returns:
        Tuple of (original_date_part, formatted_date) or None if no date found
    """
    # Get filename without extension for pure numeric check
    name_without_ext = Path(filename).stem
    
    # Check if filename (without extension) is purely numeric - this handles cases like "714.txt" from "7/14"
    if name_without_ext.isdigit():
        date_str = name_without_ext
        # Try to parse this as a date
        result = _parse_numeric_date(date_str)
        if result:
            return result
    
    # Extract numeric sequences that could be dates
    date_patterns = re.findall(r'(\d{2,5})', filename)
    
    for date_str in date_patterns:
        result = _parse_numeric_date(date_str)
        if result:
            return result
    
    return None


def generate_new_filename(original_filename: str, old_date: str, new_date: str) -> str:
    """
    Generate new filename by replacing the old date with the new formatted date.
    
    Args:
        original_filename: Original filename
        old_date: Original date string to replace
        new_date: New formatted date string
        
    Returns:
        New filename with updated date
    """
    # Replace the first occurrence of the old date with the new date
    new_filename = original_filename.replace(old_date, new_date, 1)
    return new_filename


def process_directory(directory_path: Path, logger: logging.Logger) -> List[Tuple[str, str]]:
    """
    Process all files in the given directory and rename those with date patterns.
    
    Args:
        directory_path: Path to the directory to process
        logger: Logger instance for output
        
    Returns:
        List of tuples containing (old_filename, new_filename) for renamed files
    """
    renamed_files = []
    
    if not directory_path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        return renamed_files
    
    if not directory_path.is_dir():
        logger.error(f"Path is not a directory: {directory_path}")
        return renamed_files
    
    logger.info(f"Processing directory: {directory_path}")
    
    # Get all files in the directory
    files = [f for f in directory_path.iterdir() if f.is_file()]
    logger.info(f"Found {len(files)} files to process")
    
    for file_path in files:
        filename = file_path.name
        logger.info(f"Processing file: {filename}")
        
        # Parse date from filename
        date_result = parse_date_from_filename(filename)
        
        if date_result is None:
            logger.info(f"No date pattern found in: {filename}")
            continue
        
        old_date, new_date = date_result
        new_filename = generate_new_filename(filename, old_date, new_date)
        
        if new_filename == filename:
            logger.info(f"No change needed for: {filename}")
            continue
        
        # Check if target filename already exists
        new_file_path = directory_path / new_filename
        if new_file_path.exists():
            logger.warning(f"Target filename already exists, skipping: {new_filename}")
            continue
        
        try:
            # Rename the file
            file_path.rename(new_file_path)
            logger.info(f"Renamed: {filename} -> {new_filename}")
            renamed_files.append((filename, new_filename))
            
        except OSError as e:
            logger.error(f"Failed to rename {filename}: {e}")
    
    return renamed_files


def main():
    """
    Main function to handle command line execution.
    This will be replaced by invoke tasks for CLI interface.
    """
    import sys
    
    # Default to current directory if no path provided
    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"note_retitler_{timestamp}.log"
    
    # Ask user for confirmation to save log file
    save_log = input(f"Save log file as '{log_filename}'? (y/n): ").lower().strip()
    if save_log not in ['y', 'yes']:
        print("Log file will not be saved. Proceeding with console output only.")
        log_filename = None
    
    # Setup logging
    if log_filename:
        logger = setup_logging(log_filename)
        logger.info(f"Log file will be saved as: {log_filename}")
    else:
        # Console-only logging
        logger = logging.getLogger('note_retitler')
        logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    logger.info("Starting Note Retitler Script")
    logger.info(f"Target directory: {target_path.absolute()}")
    
    # Process the directory
    renamed_files = process_directory(target_path, logger)
    
    # Summary
    logger.info(f"Processing complete. Renamed {len(renamed_files)} files.")
    
    if renamed_files:
        logger.info("Summary of renamed files:")
        for old_name, new_name in renamed_files:
            logger.info(f"  {old_name} -> {new_name}")
    
    if log_filename:
        logger.info(f"Log saved to: {log_filename}")


if __name__ == "__main__":
    main()