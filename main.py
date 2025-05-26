import os
import asyncio
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from theater import *
from datetime import date, datetime

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHATID = os.getenv("TELEGRAM_CHATID")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

async def send_periodic_msg(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"Remainder!\n"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"chat_id: {chat_id}")

    # Remove existing job
    if context.job_queue.get_jobs_by_name(str(chat_id)):
        await update.message.reply_text("Job already running")
        return
    
    # Schedule the job every 5 minutes
    context.job_queue.run_repeating(
        send_periodic_msg,
        interval=60,
        first=0,
        chat_id=chat_id,
        name=str(chat_id)
    )

    # Handle arguments(date & movie name)
    args = context.args
    if len(args) < 2:
        await update.message.reply_text(
            "/start Usage: /start 2025-05-24 Interstellar"
        )
        return
    date = args[0]
    movie_name = ' '.join(args[1:])

    # Validate date format
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        await update.message.reply_text(
            "Invalid date format. Use YYYY-MM-DD."
        )
        return

    await update.message.reply_text(
        f"Date: {date}\nMovie: {movie_name}"
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if not jobs:
        await update.message.reply_text("No active job to stop")
        return
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text("Stopped successfully")

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

def main():
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()

    # while True:
    #     movie_name = "썬더볼츠" # Need to be changed
    #     theater = Theater('01', '0013', date.today().strftime("%Y.%m.%d")) 
    #     theater.fetch_movie()
    #     movie = theater.get_movie(movie_name)
    #     if movie:
    #         await send_movie_message(movie)
    #     await asyncio.sleep(3600) # 1hour 

if __name__ == "__main__":
    main()