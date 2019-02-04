# Social platform posting
### Create post with image on vary of most popular social platforms.

## Requirements
Python >= 3.5 required.  
Install dependencies with 
```bash
pip install -r requirements.txt
```
For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

## Usage

Scrip will create a post with image for every listed social platform:   
[vk](https://vk.com), [telegram](https://telegram.org/) and [facebook](https://www.facebook.com/).

Create .env file and store your account credentials for [vk](https://vk.com),
[telegram](https://telegram.org/) and [facebook](https://www.facebook.com/).

Example of .env file provided.

For **VK** it's required to provide:
* Vk login
* Vk app id
* Vk token
* Vk album (album in group where photo will be stored)
* Vk group

For **telegram** you have to register bot and create a new channel and then provide:
* Telegram token
* Telegram chat id

For **facebook**:
* Facebook group id
* Token for Facebook Graph API

Run script with parameters:
```bash
python run.py <place_your_post_text_here> <place_image_path_here>
```