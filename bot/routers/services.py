from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from ..keyboards import services_keyboard
from ..db import SessionLocal
from ..models import Order
from ..config import settings

router = Router()

class OrderFlow(StatesGroup):
    description = State()

@router.message(F.text == "🛠 Xizmatlar")
async def services(message: Message):
    await message.answer("🛠 <b>Xizmatlar katalogi</b>\nKerakli xizmatni tanlang:", reply_markup=services_keyboard(), parse_mode="HTML")

@router.callback_query(F.data.startswith("service:"))
async def choose_service(call: CallbackQuery, state: FSMContext):
    service = call.data.split(":", 1)[1]
    await state.update_data(service=service)
    await state.set_state(OrderFlow.description)
    await call.message.answer(
        f"Tanlangan xizmat: <b>{service}</b>\n\n"
        "Loyihangiz haqida batafsil yozing. Admin siz bilan bog‘lanadi.",
        parse_mode="HTML"
    )
    await call.answer()

@router.message(OrderFlow.description)
async def create_order(message: Message, state: FSMContext):
    data = await state.get_data()
    async with SessionLocal() as session:
        order = Order(user_tg_id=message.from_user.id, service_name=data["service"],
                      description=message.text or "[Matn bo‘lmagan xabar]")
        session.add(order)
        await session.commit()
        order_id = order.id
    await state.clear()
    await message.answer(f"✅ Buyurtmangiz qabul qilindi! Raqami: #{order_id}\nTez orada siz bilan bog‘lanamiz.")
    for admin_id in settings.admin_ids:
        try:
            await message.bot.send_message(
                admin_id,
                f"🆕 <b>Yangi buyurtma #{order_id}</b>\n"
                f"Xizmat: {data['service']}\nFoydalanuvchi: {message.from_user.full_name} "
                f"(@{message.from_user.username or 'username yo‘q'})\n\n{message.text}",
                parse_mode="HTML"
            )
        except Exception:
            pass
