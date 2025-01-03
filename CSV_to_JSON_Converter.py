import csv
import json

# Dictionary for code replacements
method_codes = {
    "S": "property sold",
    "SP": "property sold prior",
    "PI": "property passed in",
    "PN": "sold prior not disclosed",
    "SN": "sold not disclosed",
    "NB": "no bid",
    "VB": "vendor bid",
    "W": "withdrawn prior to auction",
    "SA": "sold after auction",
    "SS": "sold after auction price not disclosed",
    "N/A": "price or highest bid not available"
}

type_codes = {
    "br": "bedroom(s)",
    "h": "house, cottage, villa, semi, terrace",
    "u": "unit, duplex",
    "t": "townhouse",
    "dev site": "development site",
    "o res": "other residential"
}

# Function to convert CSV to JSON with replacements
def csv_to_json(csv_file_path, json_file_path):
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            rows = []

            for row in csv_reader:
                # Replace codes with expanded forms
                if 'Method' in row and row['Method'] in method_codes:
                    row['Method'] = method_codes[row['Method']]

                if 'Type' in row and row['Type'] in type_codes:
                    row['Type'] = type_codes[row['Type']]

                rows.append(row)

        # Write the JSON file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(rows, json_file, indent=4)

        print(f"Successfully converted {csv_file_path} to {json_file_path}")

    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage
csv_file_path = 'melbourne_housing.csv'  # Input CSV file path
json_file_path = 'melbourne_housing.json'       # Output JSON file path

csv_to_json(csv_file_path, json_file_path)
