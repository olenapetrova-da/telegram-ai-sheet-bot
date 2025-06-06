### File: sheets_writer.py

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()

SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
GOOGLE_CREDS_FILE = os.getenv("GOOGLE_CREDENTIALS_JSON")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

def write_to_sheet(data):
    row = [data.get("name"), data.get("date"), data.get("location"), data.get("quantity")]
    sheet.append_row(row)
