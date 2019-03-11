import os

img_directory = os.path.join('static', 'img')
os.makedirs(img_directory, exist_ok=True)

article_directory = os.path.join('static', 'article')
os.makedirs(article_directory, exist_ok=True)

google_scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

service_account_credentials = os.getenv('GOOGLE_SERVICE_ACCOUNT_CREDENTIALS')

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

spreadsheet_id = os.getenv('SPREADSHEET_ID')

timeout_sec = os.getenv('TIMEOUT_SEC')
