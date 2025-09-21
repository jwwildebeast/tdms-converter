#!/usr/bin/env python3
"""
TDMS Batch Converter

This script processes multiple TDMS files in a directory structure and converts them to CSV format.
It recursively searches through subdirectories to find all .tdms files and converts each one,
saving the resulting CSV files in the same directory as the source TDMS files.

Usage:
    python batches.py <root_directory>

Example:
    python batches.py "C:/data/measurements"

The script will:
1. Search for all .tdms files in the specified directory and its subdirectories
2. Convert each TDMS file to CSV format using the existing conversion logic
3. Save CSV files in the same directory as their source TDMS files
4. Handle errors gracefully and provide progress feedback
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple
from nptdms import TdmsFile
import numpy as np


def find_tdms_files(root_directory: str) -> List[Path]:
    """
    Recursively find all .tdms files in the given directory and its subdirectories.
    
    Args:
        root_directory (str): Root directory to search for TDMS files
        
    Returns:
        List[Path]: List of Path objects pointing to found TDMS files
    """
    root_path = Path(root_directory)
    
    if not root_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {root_directory}")
    
    if not root_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {root_directory}")
    
    # Recursively find all .tdms files
    tdms_files = list(root_path.rglob("*.tdms"))
    
    return tdms_files


def construct_destination_file_path(
    source_file_path: Path,
    group_name: str,
    destination_file_format: str = "csv"
) -> Path:
    """
    Construct destination file path in the same directory as the source file.
    
    Args:
        source_file_path (Path): Path to the source TDMS file
        group_name (str): Name of the group within the TDMS file
        destination_file_format (str): Output file format (default: "csv")
        
    Returns:
        Path: Full path for the destination file
    """
    destination_dir = source_file_path.parent
    destination_file_name = f"{source_file_path.stem}_{group_name}.{destination_file_format}"
    return destination_dir / destination_file_name


def convert_tdms_file(source_file_path: Path) -> Tuple[bool, str, List[str]]:
    """
    Convert a single TDMS file to CSV format.
    
    This function replicates the conversion logic from the existing Worker.tdms_convertor method
    but without the PyQt5 threading and signal components.
    
    Args:
        source_file_path (Path): Path to the TDMS file to convert
        
    Returns:
        Tuple[bool, str, List[str]]: 
            - Success status (True/False)
            - Error message (if any)
            - List of created CSV files
    """
    created_files = []
    
    try:
        print(f"  Processing: {source_file_path.name}")
        
        with TdmsFile.open(str(source_file_path)) as tdms_file:
            groups = list(tdms_file.groups())
            
            if not groups:
                return False, "No groups found in TDMS file", []
            
            for group_idx, group in enumerate(groups, 1):
                print(f"    Converting group {group_idx}/{len(groups)}: {group.name}")
                
                # Convert group to DataFrame
                group_df = group.as_dataframe()
                
                if group_df.empty:
                    print(f"      Warning: Group '{group.name}' is empty, skipping")
                    continue
                
                # Construct destination file path
                csv_file_path = construct_destination_file_path(
                    source_file_path, group.name
                )
                
                # Split data into segments for memory efficiency (similar to original code)
                segments = np.array_split(group_df.index, 101)
                
                for count, chunk in enumerate(segments):
                    if count == 0:
                        # Write header and first chunk
                        group_df.loc[chunk].to_csv(
                            csv_file_path,
                            sep=",",
                            mode="w",
                            index=True,
                        )
                    else:
                        # Append remaining chunks without header
                        group_df.loc[chunk].to_csv(
                            csv_file_path,
                            header=None,
                            sep=",",
                            mode="a",
                            index=True,
                        )
                
                created_files.append(str(csv_file_path))
                print(f"      Created: {csv_file_path.name}")
        
        return True, "", created_files
        
    except Exception as e:
        error_msg = f"Error converting {source_file_path.name}: {str(e)}"
        print(f"    ERROR: {error_msg}")
        return False, error_msg, created_files


def batch_convert_tdms_files(root_directory: str) -> None:
    """
    Main function to batch convert all TDMS files in a directory structure.
    
    Args:
        root_directory (str): Root directory containing TDMS files
    """
    print(f"TDMS Batch Converter")
    print(f"=" * 50)
    print(f"Searching for TDMS files in: {root_directory}")
    
    try:
        # Find all TDMS files
        tdms_files = find_tdms_files(root_directory)
        
        if not tdms_files:
            print("No TDMS files found in the specified directory.")
            return
        
        print(f"Found {len(tdms_files)} TDMS file(s)")
        print()
        
        # Process each file
        total_files = len(tdms_files)
        successful_conversions = 0
        failed_conversions = 0
        total_csv_files_created = 0
        
        for file_idx, tdms_file in enumerate(tdms_files, 1):
            print(f"[{file_idx}/{total_files}] Converting: {tdms_file}")
            
            success, error_msg, created_files = convert_tdms_file(tdms_file)
            
            if success:
                successful_conversions += 1
                total_csv_files_created += len(created_files)
                print(f"  ✓ Successfully converted {len(created_files)} group(s)")
            else:
                failed_conversions += 1
                print(f"  ✗ Failed: {error_msg}")
            
            print()
        
        # Summary
        print("=" * 50)
        print("BATCH CONVERSION SUMMARY")
        print("=" * 50)
        print(f"Total TDMS files processed: {total_files}")
        print(f"Successful conversions: {successful_conversions}")
        print(f"Failed conversions: {failed_conversions}")
        print(f"Total CSV files created: {total_csv_files_created}")
        
        if failed_conversions == 0:
            print("\n🎉 All files converted successfully!")
        elif successful_conversions > 0:
            print(f"\n⚠️  {successful_conversions} files converted with {failed_conversions} failures")
        else:
            print("\n❌ No files were successfully converted")
            
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python batches.py <root_directory>")
        print()
        print("Example:")
        print('  python batches.py "C:/data/measurements"')
        print()
        print("This script will recursively search for .tdms files in the specified")
        print("directory and convert them to CSV format, saving the results in the")
        print("same directory as each source file.")
        sys.exit(1)
    
    root_directory = sys.argv[1]
    
    # Validate that the directory exists
    if not os.path.exists(root_directory):
        print(f"Error: Directory does not exist: {root_directory}")
        sys.exit(1)
    
    if not os.path.isdir(root_directory):
        print(f"Error: Path is not a directory: {root_directory}")
        sys.exit(1)
    
    # Run the batch conversion
    batch_convert_tdms_files(root_directory)


if __name__ == "__main__":
    main()
