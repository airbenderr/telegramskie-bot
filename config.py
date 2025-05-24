import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = "deepseek/deepseek-chat"
    SYSTEM_PROMPT = "Ты полезный, вежливый и информативный ассистент. Отвечай на русском языке."
    TEMPERATURE = 0.7
    CONTEXT_LENGTH = 10
    HTTP_REFERER = "https://github.com/your-username/your-repo"
