from urllib.parse import parse_qs

from googleapiclient.discovery import Resource

from urlextract import URLExtract
import pandas as pd

extractor = URLExtract()

days_of_week = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6,
}


def extract_id_from_google_drive_url(google_drive_url: str):
    res = parse_qs(google_drive_url)
    if not res:
        return None
    for key, value in res.items():
        return value[0]


def extract_url_from_text(text: str):
    urls = extractor.find_urls(text)
    if urls:
        return urls[0]
    return None


def extract_google_drive_id_from_text(text: str):
    url = extract_url_from_text(text)
    if url is None:
        return None
    return extract_id_from_google_drive_url(url)


def extract_boolean_value(val: str):
    if val.lower() == 'нет':
        return False
    elif val.lower() == 'да':
        return True
    return None


def parse_spreadsheet(google_spreadsheet_service: Resource, spreadsheet_id: str):
    sheet = google_spreadsheet_service.spreadsheets()

    social_platform_headers_range = 'A2:C2'
    data_headers_range = 'D1:H1'
    data_range = 'A3:H14'
    first_data_row = 3
    last_data_row = 14

    headers_social = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range=social_platform_headers_range)
        .execute()
    )
    headers_data = (
        sheet.values()
        .get(spreadsheetId=spreadsheet_id, range=data_headers_range)
        .execute()
    )

    headers = [*headers_social['values'][0], *headers_data['values'][0]]

    data = (
        sheet.values()
        .get(
            spreadsheetId=spreadsheet_id, range=data_range, valueRenderOption='FORMULA'
        )
        .execute()
    )
    df = pd.DataFrame(columns=headers, data=data['values'])
    df = df.rename(
        columns={
            'ВКонтакте': 'vk',
            'Телеграм': 'telegram',
            'Фейсбук': 'facebook',
            'День публикации': 'publish_day',
            'Время публикации': 'publish_time',
            'Статья': 'article_id',
            'Картинки': 'image_id',
            'Опубликовано?': 'is_published',
        }
    )

    df['vk'] = df['vk'].apply(extract_boolean_value)
    df['telegram'] = df['telegram'].apply(extract_boolean_value)
    df['facebook'] = df['facebook'].apply(extract_boolean_value)
    df['publish_day'] = df['publish_day'].apply(lambda x: days_of_week[x])
    df['publish_time'] = df['publish_time']
    df['article_id'] = df['article_id'].apply(extract_google_drive_id_from_text)
    df['image_id'] = df['image_id'].apply(extract_google_drive_id_from_text)
    df['is_published'] = df['is_published'].apply(extract_boolean_value)
    df['target_column'] = [
        f'H{index}' for index in range(first_data_row, last_data_row + 1)
    ]

    return df


def mark_row_as_published(
    google_spreadsheet_service: Resource, spreadsheet_id: str, row_range: str
):
    sheet = google_spreadsheet_service.spreadsheets()
    result = (
        sheet.values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=row_range,
            valueInputOption='RAW',
            body={'majorDimension': 'COLUMNS', 'values': [['да']]},
        )
        .execute()
    )
