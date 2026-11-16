from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from ..config import settings

router = Router()

class ContactFlow(StatesGroup):
    message = State()

@router.message(F.text == "📩 Murojaat")
async def contact_start(message: Message, state: FSMContext):
    await state.set_state(ContactFlow.message)
    await message.answer("Murojaatingizni yozing. Xabaringiz administratorlarga yuboriladi.")

@router.message(ContactFlow.message)
async def contact_send(message: Message, state: FSMContext):
    await state.clear()
    sent = 0
    for admin_id in settings.admin_ids:
        try:
            await message.bot.send_message(
                admin_id,
                f"📩 <b>Yangi murojaat</b>\n"
                f"Ism: {message.from_user.full_name}\n"
                f"ID: <code>{message.from_user.id}</code>\n"
                f"Username: @{message.from_user.username or 'yo‘q'}\n\n"
                f"{message.text or '[Matn bo‘lmagan xabar]'}",
                parse_mode="HTML"
            )
            sent += 1
        except Exception:
            pass
    await message.answer("✅ Murojaatingiz yuborildi." if sent else "Murojaat qabul qilindi, lekin adminlarga yetkazishda xatolik bo‘ldi.")
