#This file loops over each Excel row and creates conditions based on given data 
import configparser
import pandas as pd
from data_loader import load_and_validate_excel
from alert_creator import create_alert

# Read config.ini to get Excel input file path
config = configparser.ConfigParser()
config.read('config.ini')

try:
    file_path = config['INPUT']['excel_file_path']
except KeyError:
    print("ERROR: 'INPUT' not found under [API] in config.ini.")
    exit(1)

# Load and validate Excel data
try:
    print("Loading Excel data...")
    #data = load_and_validate_excel(file_path)
    data = load_and_validate_excel(file_path)
    print(f"Loaded {len(data)} rows from Excel.")
except Exception as e:
    print(f"Failed to load Excel: {e}")
    exit(1)


results = []

for index, row in data.iterrows():
    try:
        print(f"\nProcessing row {index + 1}...")
        result = create_alert(row, index + 1)
        print(f"Success: Alert created for row {index + 1}, ID: {result['id']}")
        results.append({
            "Row": index + 1,
            "Widget": row["NAME_OF_WIDGET"],
            "Condition Name": row["CONDITION_NAME"],
            "Status": "Success",
            "Alert ID": result["id"]
        })
    except Exception as e:
        print(f"Alert creation failed for row {index + 1}: {e}")
        results.append({
            "Row": index + 1,
            "Widget": row["NAME_OF_WIDGET"],
            "Condition Name": row["CONDITION_NAME"],
            "Status": "Failed",
            "Error": str(e)
        })

print("\nSummary:")
for r in results:
    print(r)

pd.DataFrame(results).to_excel("alert_creation_summary.xlsx", index=False)
print("\nSummary saved to alert_creation_summary.xlsx")
