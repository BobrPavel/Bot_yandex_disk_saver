import os
from datetime import datetime

from aiogram.types import Message

import yadisk

from common.bot_container import bot


SAVE_DIR = "media"
os.makedirs(SAVE_DIR, exist_ok=True)

# client = yadisk.YaDisk(token="you_token")
yandex_client = yadisk.AsyncClient(token=os.getenv("YANDEX_TOKEN"))
# print(yandex_client.check_token())


async def save_media(message: Message):
    if message.photo:
        media = message.photo[-1]
        ext = ".jpg"
    elif message.video:
        media = message.video
        ext = ".mp4"
    else:
        return

    file_id = media.file_id
    file_name = f"{file_id}{ext}"

    now = datetime.now()
    folder_name = f"{now.month} {now.year}"
    yandex_folder = f"/media/{folder_name}"
    yandex_path = f"{yandex_folder}/{file_name}"
    local_path = os.path.join(SAVE_DIR, file_name)

    # Создаем папку на Яндекс.Диске, если не существует
    if not await yandex_client.is_dir(yandex_folder):
        yandex_client.mkdir(yandex_folder)

    # Если файл уже существует на Яндекс.Диске — выходим
    if await yandex_client.is_file(yandex_path):
        return

    # Загружаем файл
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, local_path)

    # Загружаем на Яндекс.Диск
    await yandex_client.upload(local_path, yandex_path)

    # Удаляем локальный файл
    try:
        os.remove(local_path)
    except FileNotFoundError:
        pass
