import pandas as pd
import re
from datetime import datetime
import argparse
import sys

def detect_encoding(file_path):
    """
    Since I get different CSV encodings from Salesforce, this runs through various types
    to make sure it's running the correct type.
    """
    encodings_to_try = ['cp1252', 'windows-1252', 'latin-1', 'iso-8859-1', 'utf-8', 'utf-16']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # read entire file to make sure encoding works
                content = f.read()

            df = pd.read_csv(file_path, encoding=encoding, nrows=5)
            print(f"Encoding: {encoding}")
            return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            # if we get an error, try the next encoding type
            continue

    return None

def detect_date_columns(df):
    """
    Datetime columns from the GMS usually contain dates in the format 'M/D/YYYY, H:MM AM/PM'
    so we search for columns that use that pattern. May need to adjust for other formats in the
    future.
    """
    date_columns = []
    date_pattern = r'\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2} [AP]M'
    
    for column in df.columns:
        sample_values = df[column].dropna().head(5)
        
        for value in sample_values:
            if isinstance(value, str) and re.match(date_pattern, value):
                date_columns.append(column)
                break
    
    return date_columns

def convert_date_format(date_str):
    """
    Convert from 'M/D/YYYY, H:MM AM/PM' to 'YYYY-MM-DD'
    We can adjust the function to output different formats if needed.
    """
    try:
        date_obj = datetime.strptime(date_str, '%m/%d/%Y, %I:%M %p')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return date_str

def convert_csv_dates(input_file, output_file=None):
    """
    Convert dates in CSV file from 'M/D/YYYY, H:MM AM/PM' to 'YYYY-MM-DD' format
    """
    try:
        encoding = detect_encoding(input_file)
        
        if encoding is None:
            return

        df = pd.read_csv(input_file, encoding=encoding)

        date_columns = detect_date_columns(df)
        
        if not date_columns:
            print("No date columns found in the expected format 'M/D/YYYY, H:MM AM/PM'")
            print("\nColumns found in the file:")
            for col in df.columns:
                sample_value = df[col].dropna().head(1).values
                if len(sample_value) > 0:
                    print(f"  - {col}: {sample_value[0]}")
            return
        
        print(f"Found date columns: {date_columns}")

        for column in date_columns:
            print(f"Converting dates in column: {column}")
            df[column] = df[column].apply(lambda x: convert_date_format(x) if pd.notna(x) else x)

        if output_file is None:
            # create output filename with '_fixed'
            if '.' in input_file:
                base_name = input_file.rsplit('.', 1)[0]
                extension = input_file.rsplit('.', 1)[1]
                output_file = f"{base_name}_fixed.{extension}"
            else:
                output_file = f"{input_file}_fixed"

        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Successfully converted dates. Saved to: {output_file}")
        
        # sample of converted data
        print("\nSample of converted data:")
        for column in date_columns:
            print(f"\n{column}:")
            sample_dates = df[column].dropna().head(3)
            for i, date in enumerate(sample_dates):
                print(f"  Row {i+1}: {date}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTip: Make sure your file is a valid CSV and pandas is installed.")
        print("You might need to install pandas with: pip install pandas")

def main():
    parser = argparse.ArgumentParser(description='Convert date formats in CSV files')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Show which columns would be converted without making changes')
    
    args = parser.parse_args()
    
    if args.dry_run:
        # dry run mode - just show what would be converted
        try:
            print(f"Detecting encoding for {args.input_file}...")
            encoding = detect_encoding(args.input_file)
            
            if encoding is None:
                print("Could not detect a suitable encoding.")
                return
            
            print(f"File encoding: {encoding}")
            df = pd.read_csv(args.input_file, encoding=encoding)
            date_columns = detect_date_columns(df)
            
            if date_columns:
                print("\nDate columns that would be converted:")
                for column in date_columns:
                    print(f"  - {column}")
                    sample = df[column].dropna().iloc[0]
                    print(f"    Sample: {sample}")
                    print(f"    Would become: {convert_date_format(sample)}")
            else:
                print("\nNo date columns found in the expected format.")
                print("\nColumns found:")
                for col in df.columns:
                    sample_value = df[col].dropna().head(1).values
                    if len(sample_value) > 0:
                        print(f"  - {col}: {sample_value[0]}")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        convert_csv_dates(args.input_file, args.output)

if __name__ == "__main__":
    main()