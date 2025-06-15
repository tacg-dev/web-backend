import os.path

from google.auth.transport.requests import Request
from google.oauth2 import service_account

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one directory and find the file
key_path = os.path.join(os.path.dirname(script_dir), 'service_account_key.json')

creds = service_account.Credentials.from_service_account_file(
    key_path, scopes=SCOPES
)

# The ID and range of your spreadsheet
SPREADSHEET_ID = "1wcDof33bYHcyo31kDVFBMRBqy61RyKnVlNTAanm5pHg"

# Options for reading all data from worksheet1:
# Option 1: Read everything in worksheet1
RANGE_NAME = "Form Responses 1"

# Option 2: If you want to skip headers (assuming headers in row 1)
# RANGE_NAME = "worksheet1!A2:Z"

# Option 3: If you know the exact columns (e.g., A through H)
# RANGE_NAME = "worksheet1!A:H"

try:
    # Build the service
    service = build("sheets", "v4", credentials=creds)
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID, 
        range=RANGE_NAME
    ).execute()
    
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        print(f'Found {len(values)} rows of data')
        
        # Print the data (or process it as needed)
        for row in values:
            print(row)
            
        # Or convert to list of dictionaries (assuming first row is headers)
        if len(values) > 0:
            headers = values[0]
            data = []
            for row in values[1:]:  # Skip header row
                # Pad row with empty strings if it's shorter than headers
                padded_row = row + [''] * (len(headers) - len(row))
                row_dict = dict(zip(headers, padded_row))
                data.append(row_dict)
            
            print(f"\nFormatted as dictionaries:")
            for member in data[:3]:  # Print first 3 as example
                print(member)
                
except HttpError as err:
    print(f'An error occurred: {err}')