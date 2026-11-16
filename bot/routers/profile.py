from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select, func
from ..db import SessionLocal
from ..models import User, Order, ChatMessage

router = Router()

@router.message(F.text == "👤 Profil")
async def profile(message: Message):
    async with SessionLocal() as session:
        user = (await session.execute(select(User).where(User.tg_id == message.from_user.id))).scalar_one_or_none()
        orders = (await session.execute(select(func.count(Order.id)).where(Order.user_tg_id == message.from_user.id))).scalar_one()
    await message.answer(
        f"👤 <b>Profilingiz</b>\n\n"
        f"Ism: {message.from_user.full_name}\n"
        f"Username: @{message.from_user.username or 'yo‘q'}\n"
        f"Telegram ID: <code>{message.from_user.id}</code>\n"
        f"Buyurtmalar: {orders}",
        parse_mode="HTML"
    )
