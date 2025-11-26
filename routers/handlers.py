import tracemalloc
import asyncio
from aiogram import Router, F, types
from aiogram.types import FSInputFile, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

from config import photo_path, ADMIN, CHANNEL_ID, CHANNEL_INVITE
from keyboards.keyboards import *
from backend.snos import *
from backend.database import *
from backend.buySub import *

tracemalloc.start()

router = Router()
photo = FSInputFile(photo_path)

# ---- Проверка подписки ----
async def check_subscription(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False


# --- состояния ---
class States(StatesGroup):
    VIOLATIONLINK = State()
    GIVESUBID = State()
    GIVESUBDAYS = State()
    CLOSESUB = State()


# ==================== START ====================
@router.message(CommandStart())
async def start(message: Message, bot):
    user_id = message.from_user.id

    # --- проверяем подписку ---
    if not await check_subscription(bot, user_id):
        kb = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔗 Подписаться", url=CHANNEL_INVITE)],
            [types.InlineKeyboardButton(text="♻ Проверить", callback_data="check_sub")]
        ])
        await message.answer(
            "Чтобы пользоваться ботом — подпишись на канал 👇",
            reply_markup=kb
        )
        return

    # --- если подписан, запускаем твой старый код ---
    await checkUser(userid=user_id)
    subStatus = await checkSubStatus(userid=user_id)

    if subStatus:
        date = await subDate(userid=user_id)
        status = f'Активна до {date}'
    else:
        status = 'Неактивна'

    markup = markupAdmin if user_id == ADMIN else markupUser
    await message.answer_photo(
        photo=photo,
        caption=(
            f"<b>💼 Мой профиль\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"🆔 ID профиля: {user_id}\n"
            f"💎 Подписка: {status}\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖</b>"
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )


# ==================== Проверка подписки кнопка ====================
@router.callback_query(F.data == "check_sub")
async def check_sub(call: CallbackQuery, bot):
    user_id = call.from_user.id

    if await check_subscription(bot, user_id):
        await call.message.edit_text("Подписка подтверждена ✔️\nНажмите /start")
    else:
        await call.answer("❌ Нет подписки", show_alert=True)


# ==================== Остальная логика (без изменений) ====================

@router.callback_query(F.data == 'snos')
async def handlerSnos(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.answer()
    await callback.message.delete()

    if await checkSubStatus(userid=user_id) and await checkSubDate(userid=user_id):
        await callback.message.answer_photo(
            photo=photo,
            caption="<b>📝 Отправьте ссылку на нарушение</b>",
            parse_mode=ParseMode.HTML
        )
        await state.set_state(States.VIOLATIONLINK)
    else:
        await callback.message.answer_photo(
            photo=photo,
            caption="<b>❌ У вас отсутствует подписка</b>",
            parse_mode=ParseMode.HTML
        )

# — и вся остальная логика без изменений ниже —
# SNOS, ADMIN PANEL, BUY SUB, SUBSCRIPTION HANDLERS
# Я ничего не трогал
