from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL_ID
from database.users_db import add_user, count_users

router = Router()


async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False


@router.message(F.text == "/start")
async def cmd_start(message: types.Message, bot):

    # запоминаем пользователя
    add_user(message.from_user.id)

    # проверка подписки
    if not await check_subscription(bot, message.from_user.id):
        kb = InlineKeyboardBuilder()
        kb.button(text="🔗 Подписаться", url="https://t.me/c/2415070098")
        kb.button(text="♻ Проверить", callback_data="check_sub")
        kb.adjust(1)

        await message.answer(
            "Чтобы пользоваться ботом — подпишись на канал 👇",
            reply_markup=kb.as_markup()
        )
        return

    # считаем пользователей
    total = count_users()

    await message.answer(
        f"👥 Пользователей в боте: <b>{total}</b>\n\n"
        f"Добро пожаловать!"
    )


@router.callback_query(F.data == "check_sub")
async def check_sub(call: types.CallbackQuery, bot):

    if await check_subscription(bot, call.from_user.id):
        total = count_users()
        await call.message.edit_text(
            f"Подписка подтверждена ✔️\n"
            f"👥 Пользователей: <b>{total}</b>"
        )
    else:
        await call.answer("❌ Нет подписки", show_alert=True)
        
