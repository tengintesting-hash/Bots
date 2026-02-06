from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.db.shared_sqlite import add_balance, add_referral_event, create_user, get_user, is_banned, update_last_login
from app.keyboards.inline import webapp_keyboard
from app.services.deep_links import referral_link
from app.services.subscription import user_has_access

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    if await is_banned(user_id):
        await message.answer("⛔ Ваш акаунт заблоковано. Зверніться до підтримки.")
        return

    referrer_id = None
    if message.text and "ref_" in message.text:
        try:
            referrer_id = int(message.text.split("ref_")[-1])
        except ValueError:
            referrer_id = None

    existing = await get_user(user_id)
    if not existing:
        await create_user(user_id, username, referrer_id)
        if referrer_id and referrer_id != user_id:
            await add_balance(referrer_id, 1000)
            await add_referral_event(referrer_id, user_id, 1000)

    await update_last_login(user_id)

    access, missing = await user_has_access(message.bot, user_id)
    if not access:
        text_lines = ["⛔ Доступ заборонено! Підпишись на спонсорів:"]
        for channel in missing:
            title = channel.get("title") or "Канал"
            link = channel.get("link") or ""
            text_lines.append(f"- {title}: {link}")
        await message.answer("\n".join(text_lines))
        return

    await message.answer("✅ Ласкаво просимо!", reply_markup=webapp_keyboard())
    await message.answer("Команда /ref — отримати реферальне посилання.")


@router.message(Command("ref"))
async def referral_handler(message: Message):
    user_id = message.from_user.id
    if await is_banned(user_id):
        await message.answer("⛔ Ваш акаунт заблоковано. Зверніться до підтримки.")
        return
    await message.answer(
        f"Ваше реферальне посилання: {referral_link(user_id)}",
    )
