import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from config import Config
from llm import query_llm, reset_context

# Настройка логгирования в файл
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()  # Также вывод в консоль
    ]
)

logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(
    token=Config.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    reset_context(message.from_user.id)
    await message.answer(
        "🤖 <b>Привет!</b>\n"
        "Я AI-помощник. Задай мне любой вопрос.\n\n"
        "📌 Команды:\n"
        "/start или /help — справка\n"
        "/clear — сброс диалога"
    )

@dp.message(Command("clear"))
async def clear_chat(message: types.Message):
    reset_context(message.from_user.id)
    await message.answer("🔄 Контекст диалога сброшен.")

@dp.message()
async def handle_text(message: types.Message):
    if not message.text:
        return
    await bot.send_chat_action(message.chat.id, "typing")
    response = await query_llm(message.from_user.id, message.text)
    await message.answer(response)

async def main():
    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен.")
