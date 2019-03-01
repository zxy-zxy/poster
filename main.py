import datetime
import time
import os

from dotenv import load_dotenv

from utils.google_services import (
    initialize_google_drive_service,
    initialize_google_spreadsheet_service,
)

if __name__ == '__main__':
    load_dotenv()

    img_directory = os.path.join('static', 'img')
    os.makedirs(img_directory, exist_ok=True)

    article_directory = os.path.join('static', 'article')
    os.makedirs(article_directory, exist_ok=True)

    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    seconds_to_sleep = int(os.getenv('SECONDS_TO_SLEEP'))

    google_scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]

    service_account_credentials = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')

    spreadsheet_service = initialize_google_spreadsheet_service(
        google_scope, service_account_credentials
    )

    driver_service = initialize_google_drive_service(google_scope, service_account_credentials)
