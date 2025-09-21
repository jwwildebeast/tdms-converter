# TDMS Batch Converter Usage Guide

The `batches.py` script allows you to automatically convert multiple TDMS files to CSV format. It processes entire directory structures containing TDMS files and their subdirectories.

## Prerequisites

Before using the batch converter, ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

This will install:
- npTDMS==1.4.0
- numpy==1.22.3
- pandas==1.4.2
- PyQt5==5.15.4

## Usage

```bash
python batches.py <root_directory>
```

### Example

```bash
python batches.py "C:/data/measurements"
```

## What the script does

1. **Directory Traversal**: Recursively searches through the specified directory and all its subdirectories to find `.tdms` files
2. **File Processing**: For each TDMS file found, the script:
   - Opens the TDMS file using the same logic as the main GUI application
   - Processes each group within the TDMS file
   - Converts each group to CSV format
   - Saves the CSV files in the same directory as the source TDMS file
3. **Naming Convention**: Output CSV files are named as `{original_filename}_{group_name}.csv`
4. **Progress Tracking**: Displays progress and status information during conversion
5. **Error Handling**: Continues processing other files even if some conversions fail

## Example Directory Structure

**Before conversion:**
```
data/
├── experiment1/
│   ├── measurement1.tdms
│   └── measurement2.tdms
├── experiment2/
│   └── test.tdms
└── calibration/
    ├── cal1.tdms
    └── cal2.tdms
```

**After conversion:**
```
data/
├── experiment1/
│   ├── measurement1.tdms
│   ├── measurement1_Group1.csv
│   ├── measurement1_Group2.csv
│   ├── measurement2.tdms
│   └── measurement2_Data.csv
├── experiment2/
│   ├── test.tdms
│   ├── test_Group1.csv
│   └── test_Group2.csv
└── calibration/
    ├── cal1.tdms
    ├── cal1_Calibration.csv
    ├── cal2.tdms
    └── cal2_Results.csv
```

## Features

- **Non-destructive**: Original TDMS files are preserved
- **Memory efficient**: Uses chunked processing for large files
- **Robust error handling**: Continues processing even if individual files fail
- **Progress reporting**: Shows detailed progress and summary information
- **Recursive processing**: Handles nested directory structures automatically

## Error Handling

The script handles various error conditions gracefully:
- Missing or invalid directories
- Corrupted TDMS files
- Permission issues
- Disk space problems
- Empty TDMS files or groups

Failed conversions are reported but don't stop the overall process.

## Output

The script provides detailed console output including:
- Total number of TDMS files found
- Progress for each file being processed
- Number of groups converted per file
- Final summary with success/failure counts
- List of all CSV files created

## Integration with Existing Code

The `batches.py` script uses the same conversion logic as the main GUI application but without the PyQt5 interface. It directly imports and uses the conversion functions from the existing codebase, ensuring consistent results between GUI and batch operations.