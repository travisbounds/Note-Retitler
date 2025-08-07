#!/bin/bash
# One-click installation script for Note Retitler

set -e  # Exit on any error

echo "Note Retitler - One-Click Installation"
echo "====================================="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.8 or later and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Found Python $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode
echo "Installing Note Retitler..."
pip install -e .

echo
echo "Installation complete!"
echo
echo "You can now use the tool in the following ways:"
echo
echo "1. Using invoke (recommended for development):"
echo "   source venv/bin/activate"
echo "   invoke retitle --help"
echo
echo "2. Using the installed command (after activating venv):"
echo "   source venv/bin/activate"
echo "   retitle --help"
echo
echo "3. Direct Python execution:"
echo "   source venv/bin/activate"
echo "   python3 note_retitler.py"
echo
echo "For system-wide installation (optional):"
echo "   sudo pip install -e ."
echo "   # Then you can use 'retitle' from anywhere without activating venv"
echo
echo "Run tests with:"
echo "   source venv/bin/activate"
echo "   invoke test"
echo