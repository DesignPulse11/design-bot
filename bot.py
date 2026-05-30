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

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

ADMIN_ID = 8415319221


class OrderState(StatesGroup):
    waiting_for_description = State()
    waiting_for_photo = State()


@dp.message(CommandStart())
async def start(message: Message):

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
                )
            ],

            [
                InlineKeyboardButton(
                    text="❓ FAQ",
                    callback_data="faq"
                )
            ]
        ]
    )

    await message.answer(
        "🔥 Добро пожаловать в DesignPulse!\n\n"

        "🖼 АВАТАРКИ\n"
        "▫️ Обычная — 300 ₽\n"
        "▫️ Premium — 500 ₽\n"
        "▫️ Анимированная — 1000 ₽\n\n"

        "✨ ЛОГОТИПЫ\n"
        "▫️ Минимализм — 700 ₽\n"
        "▫️ Gaming — 1200 ₽\n"
        "▫️ Premium — 2000 ₽\n\n"

        "🖼 БАННЕРЫ\n"
        "▫️ Discord / Telegram — 700 ₽\n"
        "▫️ YouTube — 1000 ₽\n"
        "▫️ Gaming — 1500 ₽\n\n"

        "🎬 ВИДЕО\n"
        "▫️ Обычный эдит — 220 ₽\n"
        "▫️ Монтаж видео — 1201 ₽\n\n"

        "😎 PREMIUM ЭМОДЗИ\n"
        "▫️ Пак из 10 эмодзи — 120 ₽\n\n"

        "💎 СЕРВИСЫ\n"
        "▫️ Faceit — 639 ₽\n"
        "▫️ CryptoBot — 703 ₽\n\n"

        "🌐 WEB-ДИЗАЙН\n"
        "▫️ Лендинг — 3000 ₽\n"
        "▫️ Дизайн сайта — 5000 ₽\n"
        "▫️ Полный UI/UX проект — по договоренности\n\n"

        "👇 Выберите услугу:",
        reply_markup=keyboard
    )


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
        "emoji": "😎 Эмодзи",
        "site": "🌐 Сайт",
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


@dp.message(OrderState.waiting_for_description)
async def get_description(message: Message, state: FSMContext):

    await state.update_data(description=message.text)

    await state.set_state(OrderState.waiting_for_photo)

    await message.answer(
        "📎 Теперь отправьте фото или референс"
    )


@dp.message(OrderState.waiting_for_photo, F.photo)
async def get_photo(message: Message, state: FSMContext):

    data = await state.get_data()

    service = data["service"]
    description = data["description"]

    text = (
        f"🔥 Новый заказ!\n\n"
        f"🛒 Услуга: {service}\n"
        f"👤 Username: @{message.from_user.username}\n"
        f"🆔 ID: {message.from_user.id}\n\n"
        f"📝 ТЗ:\n{description}"
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


@dp.callback_query(F.data == "portfolio")
async def portfolio(callback: CallbackQuery):

    await callback.message.answer(
        "🖼 Портфолио:\n\n"
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


@dp.callback_query(F.data == "reviews")
async def reviews(callback: CallbackQuery):

    await callback.message.answer(
        "⭐ Отзывы:\n\n"
        "💬 Очень быстро и качественно 🔥\n"
        "💬 Лучшая аватарка!\n"
        "💬 Сделали за пару часов!"
    )

    await callback.answer()


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
        "❓ FAQ / Помощь",
        reply_markup=keyboard
    )

    await callback.answer()


@dp.callback_query(F.data == "pay_help")
async def pay_help(callback: CallbackQuery):

    await callback.message.answer(
        "💳 Оплата происходит через CryptoBot."
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
        "2️⃣ Опишите заказ\n"
        "3️⃣ Отправьте референс\n"
        "4️⃣ Ожидайте ответ дизайнера"
    )

    await callback.answer()


@dp.callback_query(F.data == "support_help")
async def support_help(callback: CallbackQuery):

    await callback.message.answer(
        "👨‍💻 Поддержка:\n"
        "@DesignPulseSupport"
    )

    await callback.answer()


@dp.callback_query(F.data == "orders")
async def orders(callback: CallbackQuery):

    await callback.message.answer(
        f"📦 Ваш профиль\n\n"
        f"🆔 ID: {callback.from_user.id}\n"
        f"👤 Username: @{callback.from_user.username}\n\n"
        f"⏳ Статус заказов:\n"
        f"Пока заказов нет."
    )

    await callback.answer()


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
            f"📦 Статус заказа:\n\n{status}"
        )

        await message.answer("✅ Статус отправлен!")

    except:
        await message.answer(
            "❌ Использование:\n"
            "/status USER_ID статус"
        )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())