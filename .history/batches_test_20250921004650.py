#!/usr/bin/env python3
"""
Modified version of batches.py for testing without dependencies
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple

def find_tdms_files(root_directory: str) -> List[Path]:
    """
    Recursively find all .tdms files in the given directory and its subdirectories.
    """
    root_path = Path(root_directory)
    
    if not root_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {root_directory}")
    
    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_directory}")
    
    # Recursively find all .tdms files
    tdms_files = list(root_path.rglob("*.tdms"))
    
    return tdms_files

def main():
    """Main entry point for testing."""
    if len(sys.argv) != 2:
        print("Usage: python batches_test.py <root_directory>")
        print()
        print("Example:")
        print('  python batches_test.py "C:/data/measurements"')
        print()
        print("This script will recursively search for .tdms files in the specified")
        print("directory and convert them to CSV format, saving the results in the")
        print("same directory as each source file.")
        return
    
    root_directory = sys.argv[1]
    
    # Validate that the directory exists
    if not os.path.exists(root_directory):
        print(f"Error: Directory does not exist: {root_directory}")
        return
    
    if not os.path.isdir(root_directory):
        print(f"Error: Path is not a directory: {root_directory}")
        return
    
    # Test finding files
    print(f"TDMS Batch Converter (Test Mode)")
    print(f"=" * 50)
    print(f"Searching for TDMS files in: {root_directory}")
    
    try:
        tdms_files = find_tdms_files(root_directory)
        
        if not tdms_files:
            print("No TDMS files found in the specified directory.")
        else:
            print(f"Found {len(tdms_files)} TDMS file(s):")
            for tdms_file in tdms_files:
                print(f"  - {tdms_file}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()