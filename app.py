
from flask import Flask, render_template, request, jsonify, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Load credentials from file
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
with open("bibleapp-465407-949da0f4bf98.json") as f:
    creds_data = json.load(f)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, SCOPE)
client = gspread.authorize(creds)
SHEET_ID = "1oPa7ExfwCRp9nq8-e2PL6JyR9uNwqR35IfplAbg4eT0"

def get_sheet():
    return client.open_by_key(SHEET_ID).sheet1

@app.route('/')
def index():
    return 'Tamil Bible App running!'

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
