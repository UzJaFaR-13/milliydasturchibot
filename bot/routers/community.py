from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select
from ..db import SessionLocal
from ..models import User, ChatMessage
from ..keyboards import main_menu

router = Router()
chat_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚪 Chatdan chiqish")], [KeyboardButton(text="🏠 Menyu")]],
    resize_keyboard=True,
    input_field_placeholder="Umumiy chatga xabar yozing..."
)

@router.message(F.text == "💬 Umumiy chat")
async def enter_chat(message: Message):
    async with SessionLocal() as session:
        user = (await session.execute(select(User).where(User.tg_id == message.from_user.id))).scalar_one_or_none()
        if user is None:
            user = User(tg_id=message.from_user.id, username=message.from_user.username,
                        full_name=message.from_user.full_name, chat_enabled=True)
            session.add(user)
        else:
            user.chat_enabled = True
            user.username = message.from_user.username
            user.full_name = message.from_user.full_name
        await session.commit()
    await message.answer(
        "💬 <b>Milliy Dasturchilar — umumiy chat</b>\n\n"
        "Siz chatga qo‘shildingiz. Endi yuborgan xabarlaringiz boshqa faol a'zolarga yetkaziladi.\n"
        "Matn, rasm, video va fayl yuborishingiz mumkin. Chiqish uchun «🚪 Chatdan chiqish»ni bosing.",
        reply_markup=chat_menu, parse_mode="HTML"
    )

@router.message(F.text == "🚪 Chatdan chiqish")
async def leave_chat(message: Message):
    async with SessionLocal() as session:
        user = (await session.execute(select(User).where(User.tg_id == message.from_user.id))).scalar_one_or_none()
        if user:
            user.chat_enabled = False
            await session.commit()
    await message.answer("Siz umumiy chatdan chiqdingiz.", reply_markup=main_menu())

@router.message(F.text == "🏠 Menyu")
async def back_to_menu(message: Message):
    await message.answer("Asosiy menyu", reply_markup=main_menu())

@router.message()
async def relay_to_community(message: Message):
    async with SessionLocal() as session:
        sender = (await session.execute(select(User).where(User.tg_id == message.from_user.id))).scalar_one_or_none()
        if not sender or not sender.chat_enabled:
            return
        sender_name, sender_username = sender.full_name, sender.username
        session.add(ChatMessage(
            user_tg_id=message.from_user.id, username=sender_username,
            full_name=sender_name, message_type=message.content_type,
            text=message.text or message.caption
        ))
        recipients = (await session.execute(
            select(User.tg_id).where(
                User.chat_enabled == True, User.is_blocked == False,
                User.tg_id != message.from_user.id
            )
        )).all()
        await session.commit()

    label = f"👤 {sender_name}" + (f" (@{sender_username})" if sender_username else "")
    if not recipients:
        await message.answer("Xabaringiz saqlandi. Hozircha chatda boshqa faol a'zo yo‘q.")
        return
    for (recipient_id,) in recipients:
        try:
            await message.bot.send_message(recipient_id, label)
            await message.bot.copy_message(
                chat_id=recipient_id, from_chat_id=message.chat.id,
                message_id=message.message_id
            )
        except Exception:
            continue
