from aiogram import Router
from aiogram.types import ChatJoinRequest

router = Router()


@router.chat_join_request()
async def approve_join(request: ChatJoinRequest):
    await request.approve()
    await request.bot.send_message(
        request.from_user.id,
        "✅ Заявку прийнято! Поверніться до бота та натисніть /start",
    )
