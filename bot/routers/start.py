from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from ..db import SessionLocal
from ..models import User
from ..keyboards import main_menu, subscription_keyboard
from ..config import settings

router = Router()

async def save_user(tg_user):
    async with SessionLocal() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_user.id))
        user = result.scalar_one_or_none()
        if user is None:
            session.add(User(tg_id=tg_user.id, username=tg_user.username,
                             full_name=tg_user.full_name))
        else:
            user.username = tg_user.username
            user.full_name = tg_user.full_name
        await session.commit()

@router.message(CommandStart())
async def start(message: Message):
    await save_user(message.from_user)
    try:
        member = await message.bot.get_chat_member(settings.CHANNEL_ID, message.from_user.id)
        subscribed = member.status in ("member", "administrator", "creator")
    except Exception:
        subscribed = False

    if not subscribed and message.from_user.id not in settings.admin_ids:
        await message.answer(
            "Assalomu alaykum! 👋\n\nMilliy Dasturchi botiga xush kelibsiz.\nDavom etish uchun kanalimizga obuna bo‘ling.",
            reply_markup=subscription_keyboard()
        )
        return
    await message.answer(
        f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
        "Milliy Dasturchi platformasiga xush kelibsiz.\n"
        "Xizmatlar, hamjamiyat va murojaatlar shu yerda.",
        reply_markup=main_menu()
    )

@router.callback_query(F.data == "check_subscription")
async def check_subscription(call: CallbackQuery):
    try:
        member = await call.bot.get_chat_member(settings.CHANNEL_ID, call.from_user.id)
        subscribed = member.status in ("member", "administrator", "creator")
    except Exception:
        subscribed = False
    if subscribed or call.from_user.id in settings.admin_ids:
        await call.message.answer("Obuna tasdiqlandi. Xush kelibsiz! ✅", reply_markup=main_menu())
        await call.answer()
    else:
        await call.answer("Hali obuna aniqlanmadi. Kanalga obuna bo‘lib qayta tekshiring.", show_alert=True)
