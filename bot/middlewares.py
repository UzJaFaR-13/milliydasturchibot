from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from .config import settings
from .keyboards import subscription_keyboard

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # Admins can always access the bot.
        user = getattr(event, "from_user", None)
        if not user or user.id in settings.admin_ids:
            return await handler(event, data)

        # Let /start and subscription-check callback pass.
        if isinstance(event, Message) and event.text and event.text.startswith("/start"):
            return await handler(event, data)
        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)

        bot = data["bot"]
        try:
            member = await bot.get_chat_member(settings.CHANNEL_ID, user.id)
            allowed = member.status in ("member", "administrator", "creator")
        except Exception:
            allowed = False

        if not allowed:
            if isinstance(event, Message):
                await event.answer(
                    "Botdan foydalanish uchun avval kanalimizga obuna bo‘ling.",
                    reply_markup=subscription_keyboard()
                )
            elif isinstance(event, CallbackQuery):
                await event.answer("Avval kanalga obuna bo‘ling.", show_alert=True)
            return
        return await handler(event, data)
