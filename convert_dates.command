# get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$DIR"

# find CSV files in the current directory (excluding ones that end with _fixed.csv, as those have already been fixed)
CSV_FILES=($(ls *.csv 2>/dev/null | grep -v "_fixed.csv"))

# count csvs
NUM_FILES=${#CSV_FILES[@]}
	
if [ $NUM_FILES -eq 0 ]; then
	echo "No CSV files found in this directory."
	echo "Please place a CSV file in the same folder as this script."
	read -p "Press any key to continue..."
	exit 1
fi
	
# if one csv, run
if [ $NUM_FILES -eq 1 ]; then
	CSV_FILE=${CSV_FILES[0]}
	echo "Found CSV file: $CSV_FILE"
else
	# if multiple csv files exist, let user choose
	echo "Multiple CSV files found:"
	for i in "${!CSV_FILES[@]}"; do 
		echo "$((i+1)). ${CSV_FILES[$i]}"
	done
	
	read -p "Enter the number of the file you want to convert: " choice
	
	# validate choice
	if ! [[ "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -lt 1 ] || [ "$choice" -gt $NUM_FILES ]; then
		echo "Invalid choice. Exiting."
		read -p "Press any key to continue..."
		exit 1
	fi
	
	CSV_FILE=${CSV_FILES[$((choice-1))]}
fi
	
echo
echo "Converting dates in: $CSV_FILE"
echo "This will create a new file with '_fixed' added to the name."
echo
	
# run the python
if python3 date_formatter.py "$CSV_FILE"; then
	echo
	echo "SUCCESS! Date conversion completed."
	echo "Your converted file is ready!"
	
	# try to reveal the output file in Finder
	OUTPUT_FILE="${CSV_FILE%.*}_fixed.csv"
	if [ -f "$OUTPUT_FILE" ]; then
		echo "Opening the output folder..."
		open -R "$OUTPUT_FILE"
	fi
else
	echo
	echo "ERROR: Date conversion failed."
	echo "Make sure you have python and pandas installed."
fi
	
echo
read -p "Press any key to close this window."