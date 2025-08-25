import os
from datetime import datetime

from aiogram.types import Message

import yadisk
from yadisk.sessions.requests_session import RequestsSession

from common.bot_container import bot


SAVE_DIR = "media"
os.makedirs(SAVE_DIR, exist_ok=True)

# client = yadisk.YaDisk(token="you_token")
yandex_client = yadisk.Client(token=os.getenv('YANDEX_TOKEN'), session=RequestsSession())
print(yandex_client.check_token())




async def save_media(message: Message):
    if message.photo:
        # Берем самое большое фото
        media = message.photo[-1]
        ext = ".jpg"
    elif message.video:
        media = message.video
        ext = ".mp4"
    else:
        return
    file_id = media.file_id
    file_name = f"{file_id}{ext}"



    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    destination = os.path.join(SAVE_DIR, file_name)

    folder = f"{str(datetime.now().month)} {str(datetime.now().year)}"

    if not yandex_client.is_dir(f"/media/{folder}"):  
        yandex_client.mkdir(f"/media/{folder}")

    
    if yandex_client.is_file(f"/media/{folder}/{file_name}"):  
        return
    else:
        await bot.download_file(file_path, destination)
        yandex_client.upload(f"media/{file_name}", f"media/{folder}/{file_name}")
        os.remove(f"media/{file_name}")
    
