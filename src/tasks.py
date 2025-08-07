"""
Invoke tasks for Note Retitler Script

This module provides command-line interface using invoke for the note retitler functionality.
"""

from invoke import task
from pathlib import Path
from datetime import datetime
import logging

# Import our main functionality
from .note_retitler import setup_logging, process_directory


@task(help={
    'path': 'Target directory path (default: current directory)',
    'log': 'Save log file (default: ask user)',
    'yes': 'Skip all confirmations and proceed automatically',
    'force': 'Alias for --yes, skip all confirmations'
})
def retitle(ctx, path=None, log=None, yes=False, force=False):
    """
    Retitle note files by converting date formats to YYYY-MM-DD.
    
    Converts date formats in filenames:
    - MD/MDD (2-3 digits) -> YYYY-MM-DD
    - MDYY/MDDYY (4-5 digits) -> YYYY-MM-DD
    
    All dates are assumed to be from 2025.
    """
    # Handle force flag (--force is alias for --yes)
    skip_confirmations = yes or force
    
    # Determine target path
    target_path = Path(path) if path else Path.cwd()
    
    if not target_path.exists():
        print(f"Error: Directory does not exist: {target_path}")
        return
    
    if not target_path.is_dir():
        print(f"Error: Path is not a directory: {target_path}")
        return
    
    # Get file count for confirmation
    files = [f for f in target_path.iterdir() if f.is_file()]
    file_count = len(files)
    
    # Show path and file count, ask for confirmation
    print(f"Target directory: {target_path.absolute()}")
    print(f"Found {file_count} files to process")
    
    if not skip_confirmations:
        proceed = input(f"Proceed with processing {file_count} files in '{target_path}'? (y/n): ").lower().strip()
        if proceed not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    # Handle log file decision
    log_filename = None
    if log is None and not skip_confirmations:
        # Ask user for confirmation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suggested_log = f"note_retitler_{timestamp}.log"
        save_log = input(f"Save log file as '{suggested_log}'? (y/n): ").lower().strip()
        if save_log in ['y', 'yes']:
            log_filename = suggested_log
    elif log or skip_confirmations:
        # User explicitly requested log file or using force mode
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"note_retitler_{timestamp}.log"
    
    # Setup logging
    if log_filename:
        logger = setup_logging(log_filename)
        print(f"Log file will be saved as: {log_filename}")
    else:
        # Console-only logging
        logger = logging.getLogger('note_retitler')
        logger.setLevel(logging.INFO)
        logger.handlers.clear()  # Clear any existing handlers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if not skip_confirmations:
            print("Proceeding with console output only.")
    
    logger.info("Starting Note Retitler Script")
    logger.info(f"Target directory: {target_path.absolute()}")
    logger.info(f"Found {file_count} files to process")
    
    # Process the directory
    renamed_files = process_directory(target_path, logger)
    
    # Summary
    print(f"\nProcessing complete. Renamed {len(renamed_files)} files.")
    logger.info(f"Processing complete. Renamed {len(renamed_files)} files.")
    
    if renamed_files:
        print("\nSummary of renamed files:")
        logger.info("Summary of renamed files:")
        for old_name, new_name in renamed_files:
            print(f"  {old_name} -> {new_name}")
            logger.info(f"  {old_name} -> {new_name}")
    
    if log_filename:
        print(f"\nLog saved to: {log_filename}")
        logger.info(f"Log saved to: {log_filename}")


@task
def test(ctx):
    """
    Run tests for the note retitler functionality.
    """
    print("Running note retitler tests...")
    
    # Import test functions
    from .note_retitler import parse_date_from_filename, generate_new_filename
    
    # Test cases for date parsing
    test_cases = [
        # MD format (2-3 digits)
        ("note12.txt", "12", "2025-01-02"),
        ("file123.md", "123", "2025-01-23"),  # M/DD format: 1/23
        
        # Special case: 7/14 format (stripped slashes) - primary target
        ("714.txt", "714", "2025-07-14"),
        ("meeting_714.docx", "714", "2025-07-14"),
        ("notes_825.md", "825", "2025-08-25"),
        
        # Pure numeric filenames (only numbers, no other text)
        ("714.txt", "714", "2025-07-14"),
        ("1225.md", "1225", "2025-12-25"),
        ("123.docx", "123", "2025-01-23"),
        
        # MDYY format (4 digits ending in 25) - but 925 is valid M/DD
        ("doc1225.txt", "1225", "2025-12-25"),
        ("note925.md", "925", "2025-09-25"),  # Valid M/DD: 9/25
        
        # MMDD format (4 digits)
        ("file1231.txt", "1231", "2025-12-31"),
        ("note0101.md", "0101", "2025-01-01"),
        
        # MDDYY format (5 digits ending in 25)
        ("doc12225.txt", "12225", "2025-12-22"),
        ("note10125.md", "10125", "2025-10-12"),  # MM/DD/YY: 10/12/25
    ]
    
    passed = 0
    failed = 0
    
    print("\nTesting date parsing:")
    for filename, expected_old, expected_new in test_cases:
        result = parse_date_from_filename(filename)
        
        if expected_new is None:
            if result is None:
                print(f"✓ {filename} - correctly identified as no valid date")
                passed += 1
            else:
                print(f"✗ {filename} - expected no date, got {result}")
                failed += 1
        else:
            if result and result[0] == expected_old and result[1] == expected_new:
                print(f"✓ {filename} - {expected_old} -> {expected_new}")
                passed += 1
            else:
                print(f"✗ {filename} - expected ({expected_old}, {expected_new}), got {result}")
                failed += 1
    
    print(f"\nTest Results: {passed} passed, {failed} failed")
    
    # Save test results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_log_filename = f"test_results_{timestamp}.log"
    
    try:
        with open(test_log_filename, 'w') as f:
            f.write(f"Note Retitler Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for filename, expected_old, expected_new in test_cases:
                result = parse_date_from_filename(filename)
                
                if expected_new is None:
                    if result is None:
                        f.write(f"✓ PASS: {filename} - correctly identified as no valid date\n")
                    else:
                        f.write(f"✗ FAIL: {filename} - expected no date, got {result}\n")
                else:
                    if result and result[0] == expected_old and result[1] == expected_new:
                        f.write(f"✓ PASS: {filename} - {expected_old} -> {expected_new}\n")
                    else:
                        f.write(f"✗ FAIL: {filename} - expected ({expected_old}, {expected_new}), got {result}\n")
            
            f.write(f"\nSummary: {passed} passed, {failed} failed\n")
            f.write(f"Status: {'ALL TESTS PASSED' if failed == 0 else 'SOME TESTS FAILED'}\n")
        
        print(f"Test results saved to: {test_log_filename}")
        
    except Exception as e:
        print(f"Warning: Could not save test results to file: {e}")
    
    if failed == 0:
        print("All tests passed! ✓")
    else:
        print("Some tests failed. Please review the implementation.")


@task
def help_formats(ctx):
    """
    Display help information about supported date formats.
    """
    print("Note Retitler - Supported Date Formats")
    print("=" * 40)
    print()
    print("Input Formats (all assumed to be from 2025):")
    print()
    print("MD Format (2-3 digits):")
    print("  12     -> 2025-01-02  (month 1, day 2)")
    print("  123    -> 2025-12-03  (month 12, day 3)")
    print("  or")
    print("  123    -> 2025-01-23  (month 1, day 23)")
    print()
    print("MDYY Format (4 digits ending in 25):")
    print("  1225   -> 2025-01-02  (month 1, day 2, year 25)")
    print("  9325   -> 2025-09-03  (month 9, day 3, year 25)")
    print()
    print("MMDD Format (4 digits):")
    print("  1231   -> 2025-12-31  (month 12, day 31)")
    print("  0101   -> 2025-01-01  (month 1, day 1)")
    print()
    print("MDDYY Format (5 digits ending in 25):")
    print("  12225  -> 2025-12-22  (month 12, day 22, year 25)")
    print("  10125  -> 2025-10-01  (month 10, day 1, year 25)")
    print()
    print("Output Format:")
    print("  All dates are converted to YYYY-MM-DD format")
    print("  Example: 1225 in filename becomes 2025-12-25")
    print()
    print("Usage:")
    print("  invoke retitle                    # Process current directory")
    print("  invoke retitle --path /some/path  # Process specific directory")
    print("  invoke retitle --log              # Force log file creation")
    print("  invoke test                       # Run tests")
    print("  invoke help-formats               # Show this help")


def retitle_cli():
    """
    CLI entry point for system-wide installation.
    This allows the script to be called as 'retitle' from anywhere.
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Retitle note files by converting date formats to YYYY-MM-DD"
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="Target directory path (default: current directory)"
    )
    parser.add_argument(
        "-y", "--yes", 
        action="store_true", 
        help="Skip all confirmations and proceed automatically"
    )
    parser.add_argument(
        "-f", "--force", 
        action="store_true", 
        help="Alias for --yes, skip all confirmations"
    )
    parser.add_argument(
        "--log", 
        action="store_true", 
        help="Save log file"
    )
    
    args = parser.parse_args()
    
    # Call the retitle logic directly without invoke
    _retitle_direct(path=args.path, log=args.log, yes=args.yes, force=args.force)


def _retitle_direct(path=None, log=None, yes=False, force=False):
    """
    Direct retitle function without invoke dependency.
    """
    # Handle force flag (--force is alias for --yes)
    skip_confirmations = yes or force
    
    # Determine target path
    target_path = Path(path) if path else Path.cwd()
    
    if not target_path.exists():
        print(f"Error: Directory does not exist: {target_path}")
        return
    
    if not target_path.is_dir():
        print(f"Error: Path is not a directory: {target_path}")
        return
    
    # Get file count for confirmation
    files = [f for f in target_path.iterdir() if f.is_file()]
    file_count = len(files)
    
    # Show path and file count, ask for confirmation
    print(f"Target directory: {target_path.absolute()}")
    print(f"Found {file_count} files to process")
    
    if not skip_confirmations:
        proceed = input(f"Proceed with processing {file_count} files in '{target_path}'? (y/n): ").lower().strip()
        if proceed not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    # Handle log file decision
    log_filename = None
    if log is None and not skip_confirmations:
        # Ask user for confirmation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        suggested_log = f"note_retitler_{timestamp}.log"
        save_log = input(f"Save log file as '{suggested_log}'? (y/n): ").lower().strip()
        if save_log in ['y', 'yes']:
            log_filename = suggested_log
    elif log or skip_confirmations:
        # User explicitly requested log file or using force mode
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"note_retitler_{timestamp}.log"
    
    # Setup logging
    if log_filename:
        logger = setup_logging(log_filename)
        print(f"Log file will be saved as: {log_filename}")
    else:
        # Console-only logging
        logger = logging.getLogger('note_retitler')
        logger.setLevel(logging.INFO)
        logger.handlers.clear()  # Clear any existing handlers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        if not skip_confirmations:
            print("Proceeding with console output only.")
    
    logger.info("Starting Note Retitler Script")
    logger.info(f"Target directory: {target_path.absolute()}")
    logger.info(f"Found {file_count} files to process")
    
    # Process the directory
    renamed_files = process_directory(target_path, logger)
    
    # Summary
    print(f"\nProcessing complete. Renamed {len(renamed_files)} files.")
    logger.info(f"Processing complete. Renamed {len(renamed_files)} files.")
    
    if renamed_files:
        print("\nSummary of renamed files:")
        logger.info("Summary of renamed files:")
        for old_name, new_name in renamed_files:
            print(f"  {old_name} -> {new_name}")
            logger.info(f"  {old_name} -> {new_name}")
    
    if log_filename:
        print(f"\nLog saved to: {log_filename}")
        logger.info(f"Log saved to: {log_filename}")