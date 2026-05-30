import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

ADMIN_ID = 8415319221


# ================= STATES =================

class OrderState(StatesGroup):
    waiting_for_description = State()
    waiting_for_photo = State()


# ================= START =================

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):

    data = await state.get_data()

    old_message_id = data.get("menu_message")

    try:
        if old_message_id:
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=old_message_id
            )
    except:
        pass

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🎨 Аватарки",
                    callback_data="avatar"
                ),
                InlineKeyboardButton(
                    text="🖼 Баннеры",
                    callback_data="banner"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✨ Логотипы",
                    callback_data="logo"
                ),
                InlineKeyboardButton(
                    text="🔥 Аниме аватарки",
                    callback_data="anime"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🎬 Эдиты",
                    callback_data="edits"
                ),
                InlineKeyboardButton(
                    text="🎞 Монтаж",
                    callback_data="montage"
                )
            ],

            [
                InlineKeyboardButton(
                    text="😎 Премиум эмодзи",
                    callback_data="emoji"
                ),
                InlineKeyboardButton(
                    text="🌐 Создание сайта",
                    callback_data="site"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💎 CryptoBot",
                    callback_data="crypto"
                ),
                InlineKeyboardButton(
                    text="🎮 Faceit",
                    callback_data="faceit"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📦 Мои заказы",
                    callback_data="orders"
                ),
                InlineKeyboardButton(
                    text="🖼 Портфолио",
                    callback_data="portfolio"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⭐ Отзывы",
                    callback_data="reviews"
                ),
                InlineKeyboardButton(
                    text="❓ FAQ",
                    callback_data="faq"
                )
            ]
        ]
    )

    sent_message = await message.answer(
        "🔥 <b>Добро пожаловать в DesignPulse!</b>\n\n"

        "🖼️ <b>АВАТАРКИ</b>\n"
        "▫️ Статичная — 300 ₽\n"
        "▫️ Premium — 500 ₽\n"
        "▫️ Анимированная — 1000 ₽\n\n"

        "🎯 <b>ЛОГОТИПЫ</b>\n"
        "▫️ Минималистичный — 700 ₽\n"
        "▫️ Игровой — 1200 ₽\n"
        "▫️ Премиум — 2000 ₽\n\n"

        "🌌 <b>БАННЕРЫ</b>\n"
        "▫️ Discord / Telegram — 700 ₽\n"
        "▫️ YouTube — 1000 ₽\n"
        "▫️ Игровой — 1500 ₽\n\n"

        "🎬 <b>ВИДЕО</b>\n"
        "▫️ Эдит — 220 ₽\n"
        "▫️ Монтаж — 1201 ₽\n\n"

        "😎 <b>PREMIUM ЭМОДЗИ</b>\n"
        "▫️ Пак из 10 — 120 ₽\n\n"

        "💎 <b>СЕРВИСЫ</b>\n"
        "▫️ Faceit — 639 ₽\n"
        "▫️ CryptoBot — 703 ₽\n\n"

        "🌐 <b>WEB-ДИЗАЙН</b>\n"
        "▫️ Лендинг — 3000 ₽\n"
        "▫️ Дизайн сайта — 5000 ₽\n\n"

        "👇 Выберите услугу:",
        reply_markup=keyboard
    )

    await state.update_data(
        menu_message=sent_message.message_id
    )


# ================= SERVICE BUTTONS =================

@dp.callback_query(F.data.in_([
    "avatar",
    "banner",
    "logo",
    "anime",
    "edits",
    "montage",
    "emoji",
    "site",
    "crypto",
    "faceit"
]))
async def service_order(callback: CallbackQuery, state: FSMContext):

    services = {
        "avatar": "🎨 Аватарка",
        "banner": "🖼 Баннер",
        "logo": "✨ Логотип",
        "anime": "🔥 Аниме аватарка",
        "edits": "🎬 Эдит",
        "montage": "🎞 Монтаж",
        "emoji": "😎 Премиум эмодзи",
        "site": "🌐 Создание сайта",
        "crypto": "💎 CryptoBot",
        "faceit": "🎮 Faceit"
    }

    service = services[callback.data]

    await state.update_data(service=service)

    await state.set_state(OrderState.waiting_for_description)

    await callback.message.answer(
        f"{service}\n\n"
        "📝 Опишите ваш заказ:"
    )

    await callback.answer()


# ================= DESCRIPTION =================

@dp.message(OrderState.waiting_for_description)
async def get_description(message: Message, state: FSMContext):

    await state.update_data(description=message.text)

    await state.set_state(OrderState.waiting_for_photo)

    await message.answer(
        "📎 Теперь отправьте фото или референс"
    )


# ================= PHOTO =================

@dp.message(OrderState.waiting_for_photo, F.photo)
async def get_photo(message: Message, state: FSMContext):

    data = await state.get_data()

    service = data["service"]
    description = data["description"]

    username = message.from_user.username

    if username:
        username = f"@{username}"
    else:
        username = "нет username"

    text = (
        f"🔥 <b>Новый заказ!</b>\n\n"
        f"🛒 <b>Услуга:</b> {service}\n"
        f"👤 <b>Username:</b> {username}\n"
        f"🆔 <b>ID:</b> {message.from_user.id}\n\n"
        f"📝 <b>ТЗ:</b>\n{description}"
    )

    await bot.send_message(ADMIN_ID, text)

    photo = message.photo[-1].file_id

    await bot.send_photo(
        ADMIN_ID,
        photo=photo
    )

    await message.answer(
        "✅ Заказ отправлен!\n"
        "Ожидайте ответа дизайнера."
    )

    await state.clear()


# ================= WRONG PHOTO =================

@dp.message(OrderState.waiting_for_photo)
async def no_photo(message: Message):

    await message.answer(
        "❌ Отправьте именно фото."
    )


# ================= PORTFOLIO =================

@dp.callback_query(F.data == "portfolio")
async def portfolio(callback: CallbackQuery):

    await callback.message.answer(
        "🖼 <b>Портфолио:</b>\n\n"
        "🎨 Аватарки\n"
        "🖼 Баннеры\n"
        "✨ Логотипы\n"
        "🔥 Аниме аватарки\n"
        "🎬 Эдиты\n"
        "🎞 Монтаж\n"
        "😎 Premium эмодзи\n"
        "🌐 Создание сайтов"
    )

    await callback.answer()


# ================= REVIEWS =================

@dp.callback_query(F.data == "reviews")
async def reviews(callback: CallbackQuery):

    await callback.message.answer(
        "⭐ <b>Отзывы:</b>\n\n"
        "💬 Очень быстро и качественно!\n"
        "💬 Лучшая аватарка 🔥\n"
        "💬 Все сделали за пару часов!"
    )

    await callback.answer()


# ================= FAQ =================

@dp.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Оплата",
                    callback_data="pay_help"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏳ Сроки",
                    callback_data="time_help"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📦 Как заказать",
                    callback_data="order_help"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Поддержка",
                    callback_data="support_help"
                )
            ]
        ]
    )

    await callback.message.answer(
        "❓ <b>FAQ / Помощь</b>",
        reply_markup=keyboard
    )

    await callback.answer()


@dp.callback_query(F.data == "pay_help")
async def pay_help(callback: CallbackQuery):

    await callback.message.answer(
        "💳 Оплата возможна через CryptoBot."
    )

    await callback.answer()


@dp.callback_query(F.data == "time_help")
async def time_help(callback: CallbackQuery):

    await callback.message.answer(
        "⏳ Среднее время выполнения:\n"
        "от 1 часа до 24 часов."
    )

    await callback.answer()


@dp.callback_query(F.data == "order_help")
async def order_help(callback: CallbackQuery):

    await callback.message.answer(
        "📦 Как сделать заказ:\n\n"
        "1️⃣ Выберите услугу\n"
        "2️⃣ Отправьте описание\n"
        "3️⃣ Скиньте референс\n"
        "4️⃣ Ожидайте выполнение"
    )

    await callback.answer()


@dp.callback_query(F.data == "support_help")
async def support_help(callback: CallbackQuery):

    await callback.message.answer(
        "👨‍💻 Поддержка:\n"
        "@DesignPulse11"
    )

    await callback.answer()


# ================= ORDERS =================

@dp.callback_query(F.data == "orders")
async def orders(callback: CallbackQuery):

    username = callback.from_user.username

    if username:
        username = f"@{username}"
    else:
        username = "нет username"

    await callback.message.answer(
        f"📦 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: {callback.from_user.id}\n"
        f"👤 Username: {username}\n\n"
        f"⏳ Статус:\n"
        f"Ожидает обработки"
    )

    await callback.answer()


# ================= ADMIN STATUS =================

@dp.message(Command("status"))
async def set_status(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        args = message.text.split(maxsplit=2)

        user_id = int(args[1])

        status = args[2]

        await bot.send_message(
            user_id,
            f"📦 <b>Статус заказа:</b>\n\n{status}"
        )

        await message.answer("✅ Статус отправлен!")

    except:
        await message.answer(
            "❌ Использование:\n"
            "/status USER_ID статус"
        )


# ================= MAIN =================

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())