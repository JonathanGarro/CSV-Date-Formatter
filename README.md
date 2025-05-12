# CSV Date Formatter

A tool for converting date formats in CSV files from 'M/D/YYYY, H:MM AM/PM' to 'YYYY-MM-DD'.

## Overview

CSV Date Formatter is a utility that automatically detects and converts date columns in CSV files. It's particularly useful for standardizing date formats in exported data files to make them more compatible with data analysis tools. I originally built it as a way to quickly fix date formatting issues I was experiencing when exporting data from my organization's Salesforce instance.

The tool:
- Automatically detects file encoding
- Identifies columns containing dates in the format 'M/D/YYYY, H:MM AM/PM'
- Converts those dates to the ISO standard format 'YYYY-MM-DD'
- Creates a new file with '_fixed' added to the original filename

## Installation

### Prerequisites

- Python 3.x
- pandas

### Installing Dependencies

```bash
pip install pandas
```

## Usage

**Note**: I've only developed and tested this in MacOS. While the Python should work across platforms, the shell script may cause errors on PC and require slight modifications.

### Option 1: Using the Command Script (Recommended)

In order to reduce the complexity to using this utility, I've created a bash script that can be double-clicked to run the python code without the need to open Terminal. This first option walks you through that simpler process.

1. Place your CSV file(s) in the same directory as the script files
2. Double-click the `convert_dates.command` file
3. If multiple CSV files are found, select the one you want to convert
4. The script will create a new file with '_fixed' added to the name (e.g., `grants_2024_fixed.csv`)

### Option 2: Using the Python Script Directly

If the user is comfortable using Terminal and navigating to the correct directory, they can run the python code directly, passing the file name after the script name.

```bash
python date_formatter.py your_file.csv
```

With an optional output file:

```bash
python date_formatter.py your_file.csv -o output_file.csv
```

To check which columns would be converted without making changes:

```bash
python date_formatter.py your_file.csv --dry-run
```

## How It Works
1. **Encoding Detection**: The tool tries multiple encodings to find the correct one for your CSV file. I typically have the same one come out of Salesforce, but I've made this flexible to use in other contexts.
2. **Date Column Detection**: It scans the CSV to identify columns containing dates in the format 'M/D/YYYY, H:MM AM/PM'.
3. **Date Conversion**: For each identified column, it converts the dates to 'YYYY-MM-DD' format.
4. **Output**: The converted data is saved to a new CSV file, preserving all original data except for the reformatted dates.

## Example

Original CSV data:
```
"Request Number","Organization","Approval Date"
"2024-001","Example Org","2/20/2024, 9:19 AM"
```

Converted CSV data:
```
"Request Number","Organization","Approval Date"
"2024-001","Example Org","2024-02-20"
```