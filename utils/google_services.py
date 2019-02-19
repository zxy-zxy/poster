from typing import List

from googleapiclient.discovery import build
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def initialize_google_drive_service(
    google_scopes: List, service_account_credentials_filepath: str
):
    google_auth = GoogleAuth()
    google_auth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        service_account_credentials_filepath, google_scopes
    )
    service = GoogleDrive(google_auth)
    return service


def initialize_google_spreadsheet_service(
    google_scopes: List, service_account_credentials_filepath: str
):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_credentials_filepath, scopes=google_scopes
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service
