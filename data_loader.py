#This file is responsible for reading Excel and validating rows
import pandas as pd
import configparser

# Load Excel file path from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
file_path = config['INPUT']['excel_file_path']

REQUIRED_COLUMNS = [
    "NAME_OF_WIDGET",
    "ALERT_REQUIRED",
    "NRQL_QUERY",
    "POLICY_ID",
    "ACCOUNT_ID",
    "CONDITION_NAME",
    "ALERT_TITLE",
    "ALERT_DESCRIPTION",
    "WINDOW_DURATION",
    "DELAY_DURATION",
    "OPERATOR",
    "THRESHOLD",
    "THRESHOLD_DURATION",
    "PRIORITY",
    "VIOLATION_TIME_LIMIT",
]

#Load excel
def load_and_validate_excel(excel_file_path):
    df = pd.read_excel(excel_file_path)

    # Check for required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in Excel: {missing_cols}")

    # Filter rows needing alerts
    df = df[df["ALERT_REQUIRED"].astype(str).str.upper() == "Y"]

    # Validate required fields per row
    errors = []
    for idx, row in df.iterrows():
        for col in REQUIRED_COLUMNS:
            if pd.isna(row[col]) or str(row[col]).strip() == "":
                errors.append(f"Row {idx + 2}: Missing value for '{col}'")

        # Create dictionary for each valid row
        alert_data_list= []
        alert_data = {
            "NRQL_QUERY": row["NRQL_QUERY"],
            "POLICY_ID": row["POLICY_ID"],
            "ACCOUNT_ID": row["ACCOUNT_ID"],
            "CONDITION_NAME": row["CONDITION_NAME"],
            "ALERT_TITLE": row["ALERT_TITLE"],
            "ALERT_DESCRIPTION": row["ALERT_DESCRIPTION"],
            "WINDOW_DURATION": row["WINDOW_DURATION"],
            "DELAY_DURATION": row["DELAY_DURATION"],
            "OPERATOR": row["OPERATOR"],
            "THRESHOLD": row["THRESHOLD"],
            "THRESHOLD_DURATION": row["THRESHOLD_DURATION"],
            "PRIORITY": row["PRIORITY"],
            "VIOLATION_TIME_LIMIT": row["VIOLATION_TIME_LIMIT"]
        }
        alert_data_list.append(alert_data)

    if errors:
        raise ValueError("Validation errors:\n" + "\n".join(errors))

    return df
