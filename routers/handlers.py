from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CHANNEL_ID, CHANNEL_INVITE
from database.users_db import add_user, subscribe  # оставляем только нужное

router = Router()

# Функция проверки подписки
async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False

# Обработчик /start
@router.message(F.text == "/start")
async def cmd_start(message: types.Message, bot):
    user_id = message.from_user.id
    add_user(user_id)  # добавляем пользователя в базу

    # проверка подписки
    if not await check_subscription(bot, user_id):
        kb = InlineKeyboardBuilder()
        kb.button(text="🔗 Подписаться", url=CHANNEL_INVITE)
        kb.button(text="♻ Проверить", callback_data="check_sub")
        kb.adjust(1)

        await message.answer(
            "Чтобы пользоваться ботом — подпишись на канал 👇",
            reply_markup=kb.as_markup()
        )
        return

    # Пользователь подписан → выполняем старую логику бота
    subscribe(user_id)  # отмечаем подписку в базе
    # ЗДЕСЬ ОСТАВЛЯЕМ ВСЕ СТАРЫЕ ДЕЙСТВИЯ БОТА
    # Например, если раньше бот отправлял сообщения или клавиатуры — они останутся
    # Для примера оставлю просто "Старый код":
    await message.answer("Старый функционал бота запускается здесь ✅")

# Callback для кнопки "Проверить"
@router.callback_query(F.data == "check_sub")
async def check_sub(call: types.CallbackQuery, bot):
    if await check_subscription(bot, call.from_user.id):
        subscribe(call.from_user.id)  # отмечаем подписку
        await call.message.edit_text("Подписка подтверждена ✔️\nСтарый функционал бота продолжает работать ✅")
    else:
        await call.answer("❌ Нет подписки", show_alert=True)
        
