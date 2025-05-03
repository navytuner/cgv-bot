import os
import asyncio
from dotenv import load_dotenv
import telegram

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHATID = os.getenv("TELEGRAM_CHATID")

async def send_daily_message():
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        message = "당신이 오늘 진행한 업무 또는 진행 해야할 업무는?"
        await bot.send_message(chat_id=TELEGRAM_CHATID, text=message)
        print("Message sent.")
    except Exception as e:
        print(f"Failed to send message: {e}")

async def main():
    while True:
        await send_daily_message()
        await asyncio.sleep(10)  # 24 hours

if __name__ == "__main__":
    asyncio.run(main())

