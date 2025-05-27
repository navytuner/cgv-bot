import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from handler.start_handler import start
from handler.stop_handler import stop
from handler.status_handler import status

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHATID = os.getenv("TELEGRAM_CHATID")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


def main():
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()


if __name__ == "__main__":
    main()
