import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one directory and find the file
key_path = os.path.join(os.path.dirname(script_dir), 'service_account_key.json')

creds = service_account.Credentials.from_service_account_file(
    key_path, scopes=SCOPES
)


service = build('calendar', 'v3', credentials=creds)

now = datetime.datetime.utcnow().isoformat() + 'Z'

events_result = service.events().list(
    calendarId='tacg.tamu@gmail.com',
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy='startTime'
).execute()

events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
    
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    # Get title (summary)
    title = event.get('summary', 'No Title')
    
    # Get description (if available)
    description = event.get('description', 'No Description')
    
    # Get location (if available, otherwise set to TBD)
    location = event.get('location', 'TBD')
    
    print(f"{start} | {end} | {title} | {description} | {location}")



