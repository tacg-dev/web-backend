import datetime
import os
import json
from flask import Flask, jsonify, Response
from flask_cors import CORS
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

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
    


def build_links(link_str: str):
    try:
        link_str = link_str.splitlines()
        links = [link.split(",") for link in link_str]
        d = {k.strip() : v.strip() for k,v in links}
        return d
    except Exception as e:
        print(e)
        return False




@app.route('/api/sheet-data', methods=['GET'])
def get_sheet_data():
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

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

        service = build("sheets", "v4", credentials=creds)

        SPREADSHEET_ID = "1wcDof33bYHcyo31kDVFBMRBqy61RyKnVlNTAanm5pHg"
        RANGE_NAME = "Form Responses 1"

        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get('values', [])

        if not values:
            return jsonify({'error': 'No data found.'}), 404

        headers = values[0]
        data = []
        for row in values[1:]:  # Skip header row
            print(row)
            if not row:
                continue
            
            if len(row) >= 14:
                row[13] = build_links(row[13])

            
                if row[13] == False:
                    row.pop(13)
                    headers.pop(13)
            
            row_dict = dict(zip(headers, row))
                
            
            data.append(row_dict)

        return jsonify({"data": data})

    except Exception as e:
        print(e)
        
        return jsonify({"error": str(e)}), 500


@app.route('/api/active-leader-data', methods=['GET'])
def get_leader_data():
    try:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

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

        service = build("sheets", "v4", credentials=creds)

        SPREADSHEET_ID = "1kJtkbQVgIGl0YrCI0g6-w_lLYH0AZOjeIyUIMdPZa54"
        RANGE_NAME = "Form Responses 1"

        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get('values', [])

        if not values:
            return jsonify({'error': 'No data found.'}), 404

        headers = values[0]
        data = []
        for row in values[1:]:  # Skip header row
            print(row)
            if not row:
                continue
            
            if len(row) >= 15:
                row[14] = build_links(row[14])
            
                if row[14] == False:
                    row.pop(14)
                    # headers.pop(14)
                    
            row_dict = dict(zip(headers, row))
           
            
            data.append(row_dict)

        return jsonify({"data": data})

    except Exception as e:
        print(e)
        
        return jsonify({"error": str(e)}), 500

@app.route('/api/active-member/headshot/<file_id>', methods=['GET'])
def get_active_member_headshot(file_id):
    try:
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

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

        service = build('drive', 'v3', credentials=creds)

        file_metadata = service.files().get(fileId=file_id).execute()
        print(f"File name: {file_metadata.get('name')}")
        print(f"File MIME type: {file_metadata.get('mimeType')}")
        print(f"File size: {file_metadata.get('size', 'N/A')}")

        request = service.files().get_media(fileId=file_id)
        image_data = io.BytesIO()
        downloader = MediaIoBaseDownload(image_data, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        return Response(
            image_data.getvalue(),
            headers={
                'Content-Type': 'image/jpeg',
                'Cache-Control': 'public, max-age=3600',
                'Access-Control-Allow-Origin': '*'
            }
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# For local development
if __name__ == "__main__":
    app.run(debug=True)