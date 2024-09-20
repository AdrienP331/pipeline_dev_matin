import os
import sys
# Add script directory to paths python can use, to avoid import errors
script_directory = os.path.split(__file__)[0]
sys.path.append(script_directory)

import csv
import json
from pipeline import get_pipeline_root

def csv_to_json(csv_file_path):
    # Ensure the output folder exists
    output_folder = get_pipeline_root() + "/database/assets"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Open and read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Iterate over each row in the CSV
        for row in reader:
            # Convert row to JSON format
            json_data = json.dumps(row, indent=4)
            
            # Create a filename for each JSON file
            json_filename = output_folder + "/" + row["asset"] + ".json"
            
            # Remove json file if it already exists
            if os.path.exists(json_filename):
                os.remove(json_filename)

            # Write the JSON data to a file
            with open(json_filename, 'w') as json_file:
                json_file.write(json_data)

            print("Created asset entry : " + json_filename)
            print(json_data)

if __name__ == "__main__":
    csv_file_path = sys.argv[1]
    csv_to_json(csv_file_path)
