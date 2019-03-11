# Social platform posting
### Create post with image on vary of most popular social platforms.

## Requirements

This project is built in docker container.
Learn more about docker at [docker](https://docs.docker.com/) and [docker-compose](https://docs.docker.com/compose/) 
## Usage

Program will create posts with image and text taken from [Google Sheets](https://www.google.com/sheets/about/)
for every listed social platform:
[vk](https://vk.com), [telegram](https://telegram.org/) and [facebook](https://www.facebook.com/).
Program will make a publications according to schedule in the sheet.

First of all, please make a copy of this [sheet](https://drive.google.com/open?id=17r4QRW_m0clut772bRnUL-U1-JiazImiZMm43SkgS9Q)
(Data will be taken from your own copy of that sheet).

You need to create a project at [Google cloud](https://cloud.google.com/) and enable [Google Sheets](https://www.google.com/sheets/about/)
and [Google Drive](https://www.google.com/drive/) API for this project.
Then create [Google Service Account](https://cloud.google.com/iam/docs/understanding-service-accounts) for your Google project
and save credentials in directory with code file. Provide name of file with credentials in .env file. 

Create *environment.env* file and store your account credentials for [vk](https://vk.com),
[telegram](https://telegram.org/) and [facebook](https://www.facebook.com/).

Example of environment.env (as *.env.example*) file provided.

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

Run!
```bash
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml up
```



