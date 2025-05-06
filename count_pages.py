import requests
from PyPDF2 import PdfReader
from io import BytesIO

# Airtable API details
API_KEY = "https://api.airtable.com/v0/appyRiDZRQY0l813r/tbl3gupULs6kAt2wG"
BASE_ID = "appyRiDZRQY0l813r"  # Airtable base ID
TABLE_NAME = "tblBsl4btA9Ovpi13"  # Airtable table ID
FIELD_NAME = "File"  # Column name where are attachements

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_records():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    all_records = []
    offset = None

    while True:
        params = {"offset": offset} if offset else {}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_records.extend(data["records"])
        offset = data.get("offset")
        if not offset:
            break

    return all_records

def count_pages_from_url(file_url):
    response = requests.get(file_url)
    if response.status_code == 200:
        reader = PdfReader(BytesIO(response.content))
        return len(reader.pages)
    return 0

records = get_records()

for record in records:
    attachments = record['fields'].get(FIELD_NAME, [])
    for file in attachments:
        file_url = file['url']
        filename = file['filename']
        try:
            page_count = count_pages_from_url(file_url)
            print(f"{filename}: {page_count} page(s)")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
