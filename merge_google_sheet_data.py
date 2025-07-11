import os
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

load_dotenv()

# Auth setup
# Ensure each sheet is shared for service account email
# See .env file for list of Spreadsheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_CREDENTIALS_JSON"), scope)
client = gspread.authorize(creds)

# Load target sheet
target_spreadsheet = client.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
target_sheet = target_spreadsheet.sheet1

# Load all source sheet IDs
source_sheet_ids = os.getenv("SOURCE_SHEET_IDS").split(",")

for sheet_id in source_sheet_ids:
    spreadsheet = client.open_by_key(sheet_id.strip())
    location = spreadsheet.title.strip().split()[1]  # second word from spreadsheet title

    for worksheet in spreadsheet.worksheets():
        name = worksheet.title.strip()
        data = worksheet.get_all_records()

        for row in data:
            # Normalize column names (case-insensitive, fallback logic)
            row_keys = {k.lower(): k for k in row.keys()}
            get_field = lambda *keys: next((row.get(row_keys.get(k.lower(), ""), "") for k in keys if row_keys.get(k.lower(), "") in row), "")

            raw_date = get_field("date")
            try:
                cleaned_date = raw_date.replace("/", ".").replace("-", ".")
                parsed_date = datetime.strptime(cleaned_date, "%d.%m.%Y")
                date = parsed_date.strftime("%d.%m.%Y")
            except:
                try:
                    parsed_date = datetime.strptime(cleaned_date, "%Y.%m.%d")
                    date = parsed_date.strftime("%d.%m.%Y")
                except:
                    date = raw_date

            quantity = get_field("quantity", "qty", "amount")
            comments = get_field("comments", "note", "remark")
            order = get_field("order", "code")

            target_sheet.append_row([
                name,                     # from worksheet title
                date,
                location,                 # from spreadsheet name
                order,
                quantity,
                comments,
                "Google Sheet",
                datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            ])

print("✅ All data merged with flexible column detection and normalized dates.")
