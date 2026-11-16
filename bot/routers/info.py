from aiogram import Router, F
from aiogram.types import Message
from ..config import settings

router = Router()

@router.message(F.text == "🌐 Biz haqimizda")
async def about(message: Message):
    await message.answer(
        "🇺🇿 <b>Milliy Dasturchi</b>\n\n"
        "Milliy Dasturchi — IT, dasturlash, texnologiyalar va raqamli yechimlar "
        "haqidagi loyiha. Bu bot orqali xizmatlar bilan tanishishingiz, "
        "hamjamiyat chatida qatnashishingiz va murojaat yuborishingiz mumkin.\n\n"
        f"🌍 Sayt: {settings.SITE_URL}",
        parse_mode="HTML"
    )

@router.message(F.text == "🔗 Sayt")
async def website(message: Message):
    await message.answer(f"🌐 Rasmiy sayt: {settings.SITE_URL}")
