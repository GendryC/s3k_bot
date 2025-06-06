from telegram.ext import ApplicationBuilder
from bot.bot import add_handlers
from config import AppConfig
from logger import init_logger
from database.__init__ import init_db

def main():
    config = AppConfig()
    logger = init_logger(config.get("APP_MODE") != "dev")

    init_db()
    TELEGRAM_TOKEN = config.get("TELEGRAM_TOKEN")

    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not found!")
        return

    logger.info("Building app...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app = add_handlers(app)
    logger.info("App built successfully")

    logger.info("Start polling...")
    app.run_polling()
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
