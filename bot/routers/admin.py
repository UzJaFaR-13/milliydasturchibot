from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select, func
from ..config import settings
from ..db import SessionLocal
from ..models import User, Order

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids

@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return
    async with SessionLocal() as session:
        users = (await session.execute(select(func.count(User.id)))).scalar_one()
        orders = (await session.execute(select(func.count(Order.id)))).scalar_one()
        new_orders = (await session.execute(select(func.count(Order.id)).where(Order.status == "new"))).scalar_one()
    await message.answer(
        f"🛠 <b>Admin panel</b>\n\n"
        f"👥 Foydalanuvchilar: {users}\n"
        f"📦 Buyurtmalar: {orders}\n"
        f"🆕 Yangi buyurtmalar: {new_orders}\n\n"
        "Buyruqlar:\n/orders — oxirgi buyurtmalar\n/broadcast Matn — obunachilarga xabar",
        parse_mode="HTML"
    )

@router.message(Command("orders"))
async def list_orders(message: Message):
    if not is_admin(message.from_user.id):
        return
    async with SessionLocal() as session:
        rows = (await session.execute(select(Order).order_by(Order.id.desc()).limit(10))).scalars().all()
    if not rows:
        await message.answer("Hozircha buyurtmalar yo‘q.")
        return
    text = "\n\n".join([f"#{o.id} | {o.service_name}\n{o.description[:300]}\nHolat: {o.status}" for o in rows])
    await message.answer(text)

@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    body = message.text.partition(" ")[2].strip()
    if not body:
        await message.answer("Foydalanish: /broadcast Hammaga yuboriladigan xabar")
        return
    async with SessionLocal() as session:
        users = (await session.execute(select(User.tg_id).where(User.is_blocked == False))).all()
    sent = 0
    for (uid,) in users:
        try:
            await message.bot.send_message(uid, body)
            sent += 1
        except Exception:
            pass
    await message.answer(f"Xabar yuborildi: {sent} ta foydalanuvchi.")
