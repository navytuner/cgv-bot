from telegram import Update
from telegram.ext import ContextTypes
from models.theater import Theater
from datetime import datetime
from config.settings import INTERVAL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    result = await get_date_and_title(update, context)
    if not result:
        return
    date, title = result

    # Remove existing job
    if context.job_queue.get_jobs_by_name(str(chat_id)):
        await update.message.reply_text("Job already running")
        return

    try:
        theater = Theater(date=date)
        context.job_queue.run_repeating(
            fetch_and_display_movieinfo,
            interval=INTERVAL,
            first=5,  # for immediate feedback
            chat_id=chat_id,
            name=str(chat_id),
            data={"theater": theater, "title": title},
        )

    except Exception as e:
        print(f"Error starting job: {e}")
        await update.message.reply_text(
            f"**Failed to start monitoring**\n\n", parse_mode="Markdown"
        )


async def get_date_and_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("Usage: /start 2025.05.24 Interstella")
        return None

    date = args[0]
    title = " ".join(args[1:])
    print(f"date: {date}, title: {title}")

    # Validation
    try:
        date_obj = datetime.strptime(date, "%Y.%m.%d")
        if date_obj.date() < datetime.now().date():
            await update.message.reply_text(
                "The selected date is in the past. Please select date again"
            )
            return None

    except ValueError:
        await update.message.reply_text("Invalid date format. Use YYYY.MM.DD")
        return None
    return (date, title)


async def fetch_and_display_movieinfo(context: ContextTypes.DEFAULT_TYPE):
    try:
        theater = context.job.data["theater"]
        title = context.job.data["title"]

        # Fetch movie data
        theater.fetch_movie()
        movie = theater.get_movie(title)

        # Movie not found
        if not movie:
            await context.bot.send_message(
                chat_id=context.job.chat_id, text=f"Movie '{title}' not found"
            )
            return
        if not movie["plays"]:
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"No showtimes available for '{title}'",
            )
            return

        # Build message
        msg = f"{theater.get_date().strftime('%Y.%m.%d(%A)')}\n"
        msg += f"*** {movie['title']} ***\n\n"
        for play in movie["plays"]:
            msg += f"{play['time']} {play['remainSeat']}석 / {movie['totSeat']}석\n"

        await context.bot.send_message(
            chat_id=context.job.chat_id, text=msg, parse_mode="Markdown"
        )

    except KeyError as e:
        print(f"Missing key in job data: {e}")

    except Exception as e:
        print(f"Failed to send message: {e}")
