import datetime
import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

CORS(app) 

@app.route('/', )
def index():
    print("made it here")
    return "Hello, World!"


@app.route('/api/calendar-events', methods=['GET'])
def get_calendar_events():
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Similar credential handling as FastAPI example
        key_info = os.environ.get("GOOGLE_SERVICE_ACCOUNT_KEY")
        if not key_info:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            key_path = os.path.join(os.path.dirname(script_dir), 'service_account_key.json')
            creds = service_account.Credentials.from_service_account_file(
                key_path, scopes=SCOPES
            )
        else:
            key_dict = json.loads(key_info)
            creds = service_account.Credentials.from_service_account_info(
                key_dict, scopes=SCOPES
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
        
        
        formatted_events = []
        for event in events:
            full_data_start = event['start'].get('dateTime', event['start'].get('date'))
            start = full_data_start[0:10]
            time = "All Day"
            if len(full_data_start) > 10:
                time = full_data_start[11:16]
    
            
            formatted_events.append({
                'start': start,
                'time': time,
                'end': event['end'].get('dateTime', event['end'].get('date')),
                'title': event.get('summary', 'No Title'),
                'description': event.get('description', 'No Description'),
                'location': event.get('location', 'TBD')
            })
        print(formatted_events)
        return jsonify({"events": formatted_events})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For local development
if __name__ == "__main__":
    app.run(debug=True)