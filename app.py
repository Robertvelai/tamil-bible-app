
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
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SHEET_ID).sheet1
    return sheet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/archive')
def archive():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return render_template('archive.html', verses=data)

@app.route('/verses')
def verses():
    sheet = get_sheet()
    data = sheet.get_all_records()
    active = [row['Verse'] for row in data if row['IsArchived'] != 'TRUE']
    return jsonify(active)

@app.route('/add', methods=['POST'])
def add():
    from flask import request
    verse = request.form['verse']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet = get_sheet()
    sheet.append_row([verse, now, now, "TRUE"])  # Archived by default
    return jsonify({'status': 'added'})

@app.route('/update/<int:index>', methods=['POST'])
def update(index):
    from flask import request
    new_verse = request.form['verse']
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet = get_sheet()
    row = index + 2  # 1 for header, 1 for 0-based index
    sheet.update_cell(row, 1, new_verse)
    sheet.update_cell(row, 3, now)
    return jsonify({'status': 'updated'})

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete(index):
    sheet = get_sheet()
    row = index + 2
    sheet.delete_row(row)
    return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
