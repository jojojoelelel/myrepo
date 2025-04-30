# Import Libraries
import requests
import os
import csv
from tqdm import tqdm

# Folder paths
input_folder = 'input'
output_folder = 'output'

input_csv_file = os.path.join(input_folder, 'cv-valid-dev.csv')
output_csv_file = os.path.join(output_folder, 'cv-valid-dev.csv')

api_url = 'http://localhost:8001/asr'

# List to store updated records
updated_rows = []

# Open input csv file
with open(input_csv_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    # Add generated_text column to field names
    fieldnames = reader.fieldnames + ['generated_text']
    # Iterate over records in input csv file
    for row in tqdm(reader):
        # Get file path
        file_path = row['filename']
        # Call ASR API
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(api_url, files={'file': f})
                data = response.json()
                row['generated_text'] = data.get('transcription', '')
                row['duration'] = data.get('duration', '')

        except Exception as e:
            print(f"Failed on file {file_path}: {e}")
            row['generated_text'] = ''
            row['duration'] = ''

        # Append updated record to list
        updated_rows.append(row)

# Open output csv file
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    # Create writer object
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    # Write header
    writer.writeheader()
    # Write list into output csv file
    writer.writerows(updated_rows)

# Acknowledgement
print("Transcriptions saved.")