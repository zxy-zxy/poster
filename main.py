import datetime
import time
import os

from dotenv import load_dotenv

from utils.common import create_directory, read_text_from_file
from utils.google_services import (
    initialize_google_drive_service,
    initialize_google_spreadsheet_service,
)
from utils.spreadsheet_handler import SpreadSheetHandler
from utils.drive_handler import DriveHandler
from social import social_platform_object_factory


def process_spreadsheet(spreadsheet_id):
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

    spreadsheet_handler = SpreadSheetHandler(
        spreadsheet_service, spreadsheet_id=spreadsheet_id
    )

    drive_handler = DriveHandler(drive_service)

    social_platform_authorization_config = {
        'vk_login': os.getenv('VK_LOGIN'),
        'vk_app_id': os.getenv('VK_APP_ID'),
        'vk_token': os.getenv('VK_TOKEN'),
        'telegram_token': os.getenv('TELEGRAM_TOKEN'),
        'facebook_api_token': os.getenv('FACEBOOK_TOKEN'),
    }

    social_platform_post_config = {
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'vk_group_id': os.getenv('VK_GROUP_ID'),
        'vk_album_id': os.getenv('VK_ALBUM_ID'),
        'facebook_group_id': os.getenv('FACEBOOK_GROUP_ID'),
    }

    telegram_social = social_platform_object_factory.create(
        'telegram', **social_platform_authorization_config
    )
    vk_social = social_platform_object_factory.create(
        'vk', **social_platform_authorization_config
    )
    facebook_social = social_platform_object_factory.create(
        'facebook', **social_platform_authorization_config
    )

    spreadsheet_handler.parse_spreadsheet()
    df = spreadsheet_handler.df

    current_datetime = datetime.datetime.now()

    for index, row in df.iterrows():
        need_to_publish_row = all(
            [
                current_datetime.weekday() == row['publish_day'],
                current_datetime.time().hour == row['publish_time'],
                not row['is_published'],
            ]
        )
        if not need_to_publish_row:
            continue

        process_row_from_dataframe(
            row,
            spreadsheet_handler,
            drive_handler,
            social_platform_post_config,
            telegram_social,
            vk_social,
            facebook_social,
        )
        break


def process_row_from_dataframe(
    row,
    spreadsheet_handler,
    drive_handler,
    social_platform_post_config,
    telegram_social,
    vk_social,
    facebook_social,
):
    img_file_path = drive_handler.load_file_from_google_drive_to_disk(
        row['image_id'], img_directory
    )

    article_file_path = drive_handler.load_file_from_google_drive_to_disk(
        row['article_id'], article_directory, 'text/plain'
    )
    article_text = read_text_from_file(article_file_path)
    if row['telegram']:
        telegram_social.post_with_image_in_social_media(
            text=article_text, image_path=img_file_path, **social_platform_post_config
        )
    if row['vk']:
        vk_social.post_with_image_in_social_media(
            text=article_text, image_path=img_file_path, **social_platform_post_config
        )
    if row['facebook']:
        facebook_social.post_with_image_in_social_media(
            text=article_text, image_path=img_file_path, **social_platform_post_config
        )
    spreadsheet_handler.mark_row_as_published(row['target_column'])


if __name__ == '__main__':
    seconds_to_sleep = 10
    load_dotenv()

    img_directory = create_directory(os.path.join('static', 'img'))
    article_directory = create_directory(os.path.join('static', 'article'))
    spreadsheet_id = os.getenv('SPREADSHEET_ID')

    while True:
        process_spreadsheet(spreadsheet_id)
        time.sleep(seconds_to_sleep)
