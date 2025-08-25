from aiogram import F, types, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from filters.chat_types import ChatTypeFilter


from utils.save_media import save_media


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Я бот для личной автоматизации сохранения фото и видео на яндекс диск моего создателя"
    )


# Обработка фото или видео
@user_private_router.message(F.photo | F.video)
async def handle_single_media(message: Message):
    await save_media(message)


@user_private_router.message()
async def saver2(message: types.Message):
    await message.answer(
        "Пожалуйста отправьте фото или видео (можно сразу несколько одним сообщением)"
    )
