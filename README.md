# Milliy Dasturchi Telegram Bot

Python 3.12+, Aiogram 3, PostgreSQL va SQLAlchemy asosidagi modulli bot.

## Hozirgi modullar
- Kanalga obunani tekshirish
- Start va asosiy menyu
- Loyiha haqida va rasmiy sayt havolasi
- Xizmatlar katalogi va buyurtma qabul qilish
- Adminlarga murojaat yuborish
- Profil va statistika
- Admin panel, buyurtmalar ro‘yxati, broadcast
- PostgreSQL va Docker Compose\n- A’zolar ixtiyoriy qo‘shiladigan umumiy chat: matn, rasm, video va fayllarni boshqa chat a’zolariga uzatish\n- Chatdan chiqish tugmasi va xabarlar tarixini saqlash

## Muhim: umumiy chat
Ushbu boshlang‘ich versiyada umumiy chat menyusi va chatga kirish xabari mavjud, ammo xabarlarni barcha a'zolarga tarqatish (relay) hali yoqilmagan. Buni ishlab chiqarish muhitiga tayyor qilish uchun Redis orqali chatga a'zo bo‘lish holatini boshqarish, bloklash/shikoyat, flood limit, media relay va xabar tarixini qo‘shish kerak. Bu qismni ataylab yarim ishlaydigan tarzda hammaga xabar tarqatadigan qilib qo‘ymadik.

## O‘rnatish
1. Telegram'da @BotFather orqali bot yarating va token oling.
2. Botni kanalingizga administrator qiling. Kanal a'zoligini tekshirish uchun bot kanalga kirish huquqiga ega bo‘lishi kerak.
3. `.env.example` faylidan `.env` yarating:
   ```bash
   cp .env.example .env
   ```
4. `.env` ichida `BOT_TOKEN`, `CHANNEL_ID`, `CHANNEL_URL`, `ADMIN_IDS` qiymatlarini to‘ldiring.
   - `CHANNEL_ID`: ommaviy kanal bo‘lsa `@kanal_username`, private kanal bo‘lsa Telegram chat ID.
   - `ADMIN_IDS`: vergul bilan ajratilgan Telegram numeric ID'lar.
5. Ishga tushiring:
   ```bash
   docker compose up --build -d
   docker compose logs -f bot
   ```

## Lokal ishga tushirish
PostgreSQL ishga tushgan bo‘lsin, `.env` dagi `DATABASE_URL` ni moslang:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m bot.main
```

## Admin buyruqlari
- `/admin` — statistika
- `/orders` — oxirgi buyurtmalar
- `/broadcast Matn` — foydalanuvchilarga xabar yuborish

## Ishlab chiqarishdan oldin
- Umumiy chat uchun flood limit, bloklash/shikoyat va moderator vositalarini qo‘shish
- Alembic migratsiyalarini qo‘shish
- Admin rollari va buyurtma holatini boshqarish
- Privacy policy va foydalanish qoidalari
- Rate limiting, audit log va backup
- Testlar, monitoring va server secrets
- Saytning haqiqiy kontent/API bilan integratsiyasi

Bu kod ishga tushiriladigan boshlang‘ich skelet; to‘liq production-ready mahsulot deb qabul qilmang.
