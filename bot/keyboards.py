from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from .config import settings

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Biz haqimizda"), KeyboardButton(text="🛠 Xizmatlar")],
            [KeyboardButton(text="💬 Umumiy chat"), KeyboardButton(text="📩 Murojaat")],
            [KeyboardButton(text="👤 Profil"), KeyboardButton(text="🔗 Sayt")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo‘limni tanlang..."
    )

def subscription_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=settings.CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subscription")]
    ])

def services_keyboard():
    services = [
        "🌐 Web sayt yaratish", "🤖 Telegram bot yaratish",
        "⚙️ Backend va API", "📱 Mobil ilova",
        "🎨 UI/UX dizayn", "🎓 Dasturlash bo‘yicha ta’lim",
        "🖥 Server, Linux va Docker", "🛡 Texnik yordam"
    ]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=s, callback_data=f"service:{s}")] for s in services
    ])
