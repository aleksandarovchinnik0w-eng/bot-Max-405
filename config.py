import os


class Config:
    # Токен бота (получить у @BotFather)
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_bot_token_here")

    # Настройки Google Sheets
    GOOGLE_SHEETS_CREDENTIALS = "credentials/service_account.json"
    GOOGLE_SHEETS_ID = "your_google_sheets_id_here"

    # Настройки базы данных
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot_data.db")