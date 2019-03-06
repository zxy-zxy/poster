import os
import datetime

from pandas import Series

from pydrive.drive import GoogleDrive
from googleapiclient.discovery import Resource

from utils.google_services import (
    initialize_google_drive_service,
    initialize_google_spreadsheet_service,
)

from utils.spreadsheet_handler import parse_spreadsheet, mark_row_as_published
from utils.drive_handler import load_file_from_google_drive_to_disk
from utils.social import (
    telegram_post_with_image,
    vk_post_with_image,
    facebook_post_with_image,
    initialize_telegram_bot,
    initialize_vk_api,
)
from settings import (
    service_account_credentials,
    google_scope,
    social_platform_config,
    img_directory,
    article_directory,
    spreadsheet_id,
)


def process_row(row: Series, spreadsheet_service: Resource, drive_service: GoogleDrive):
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

    telegram_bot = initialize_telegram_bot(social_platform_config['telegram_token'])
    vk_api_, vk_upload_api_ = initialize_vk_api(
        social_platform_config['vk_login'],
        social_platform_config['vk_app_id'],
        social_platform_config['vk_token'],
    )

    if row['telegram']:
        telegram_post_with_image(
            telegram_bot, article_text, img_file_path, **social_platform_config
        )
    if row['vk']:
        vk_post_with_image(
            vk_api_,
            vk_upload_api_,
            article_text,
            img_file_path,
            **social_platform_config
        )

    if row['facebook']:
        facebook_post_with_image(article_text, img_file_path, **social_platform_config)

    mark_row_as_published(spreadsheet_service, spreadsheet_id, row['target_column'])


def process_spreadsheet():
    spreadsheet_service = initialize_google_spreadsheet_service(
        google_scope, service_account_credentials
    )

    drive_service = initialize_google_drive_service(
        google_scope, service_account_credentials
    )

    df = parse_spreadsheet(spreadsheet_service, spreadsheet_id)
    for index, row in df.iterrows():
        process_row(row, spreadsheet_service, drive_service)


def process_posting():
    process_spreadsheet()
