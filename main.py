import os
import time
import datetime

from dotenv import load_dotenv
from pandas import Series

from pydrive.drive import GoogleDrive
from googleapiclient.discovery import Resource

from utils.google_services import (
    initialize_google_drive_service,
    initialize_google_spreadsheet_service,
)

from utils.spreadsheet_handler import parse_spreadsheet, mark_row_as_published
from utils.drive_handler import load_file_from_google_drive_to_disk
from utils.social import post_with_image_in_social_media


def process_row(
    row: Series,
    social_platform_config: dict,
    spreadsheet_service: Resource,
    drive_service: GoogleDrive,
):
    img_file_path = load_file_from_google_drive_to_disk(
        drive_service, row['image_id'], img_directory
    )

    article_file_path = load_file_from_google_drive_to_disk(
        drive_service, row['article_id'], article_directory, 'text/plain'
    )
    with open(article_file_path, 'r') as file:
        article_text = file.read()

    current_datetime = datetime.datetime.now()

    need_to_publish_row = all(
        [
            current_datetime.weekday() == row['publish_day'],
            current_datetime.time().hour == row['publish_time'],
            not row['is_published'],
        ]
    )

    if not need_to_publish_row:
        return

    if row['facebook']:
        post_with_image_in_social_media(
            provider='facebook',
            text=article_text,
            image_path=img_file_path,
            **social_platform_config
        )
    if row['telegram']:
        post_with_image_in_social_media(
            provider='telegram',
            text=article_text,
            image_path=img_file_path,
            **social_platform_config
        )
    if row['vk']:
        post_with_image_in_social_media(
            provider='vk',
            text=article_text,
            image_path=img_file_path,
            **social_platform_config
        )

    mark_row_as_published(spreadsheet_service, spreadsheet_id, row['target_column'])


def process_spreadsheet(spreadsheet_id: str):
    google_scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]

    service_account_credentials = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')

    spreadsheet_service = initialize_google_spreadsheet_service(
        google_scope, service_account_credentials
    )

    drive_service = initialize_google_drive_service(
        google_scope, service_account_credentials
    )

    social_platform_config = {
        'vk_login': os.getenv('VK_LOGIN'),
        'vk_app_id': os.getenv('VK_APP_ID'),
        'vk_token': os.getenv('VK_TOKEN'),
        'telegram_token': os.getenv('TELEGRAM_TOKEN'),
        'facebook_api_token': os.getenv('FACEBOOK_TOKEN'),
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'vk_group_id': os.getenv('VK_GROUP_ID'),
        'vk_album_id': os.getenv('VK_ALBUM_ID'),
        'facebook_group_id': os.getenv('FACEBOOK_GROUP_ID'),
    }

    df = parse_spreadsheet(spreadsheet_service, spreadsheet_id)
    for index, row in df.iterrows():
        process_row(row, social_platform_config, spreadsheet_service, drive_service)
        break


if __name__ == '__main__':
    load_dotenv()

    img_directory = os.path.join('static', 'img')
    os.makedirs(img_directory, exist_ok=True)

    article_directory = os.path.join('static', 'article')
    os.makedirs(article_directory, exist_ok=True)

    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    seconds_to_sleep = int(os.getenv('SECONDS_TO_SLEEP'))

    while True:
        process_spreadsheet(spreadsheet_id)
        time.sleep(seconds_to_sleep)
