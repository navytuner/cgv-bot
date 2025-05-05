import os
import asyncio
from dotenv import load_dotenv
import telegram
from theater import *
from datetime import date

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHATID = os.getenv("TELEGRAM_CHATID")

async def send_movie_message(movie):
    msg = date.today().strftime("%Y.%m.%d(%A)")
    msg += "\n"
    msg += movie["title"] + "\n"
    for play in movie["plays"]:
        msg += play["time"] + " "
        msg += play["remainSeat"] + "석 / " + movie["totSeat"] + "석\n"
    try:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHATID, text=msg)
        print("Message sent")
    except Exception as e:
        print(f"Failed to send message: {e}")

async def main():
    while True:
        movie_name = "썬더볼츠" # Need to be changed
        theater = Theater('01', '0013', date.today().strftime("%Y.%m.%d")) 
        theater.fetch_movie()
        movie = theater.get_movie(movie_name)
        if movie:
            await send_movie_message(movie)
        await asyncio.sleep(3600) # 1hour 

if __name__ == "__main__":
    asyncio.run(main())

