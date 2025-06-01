from telegram import Update
from telegram.ext import ContextTypes
from models.theater import Theater
from config.settings import INTERVAL


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    result = await _get_date_and_title(update, context)
    if not result:
        return
    date, title = result

    # Remove existing job
    if context.job_queue.get_jobs_by_name(str(chat_id)):
        await update.message.reply_text("Job already running")
        return

    try:
        theater = Theater()
        context.job_queue.run_repeating(
            _fetch_and_display_movieinfo,
            interval=INTERVAL,
            first=5,  # for immediate feedback
            chat_id=chat_id,
            name=str(chat_id),
            data={"theater": theater, "title": title, "date": date},
        )

    except Exception as e:
        print(f"Error starting job: {e}")
        await update.message.reply_text(
            f"**Failed to start monitoring**\n\n", parse_mode="Markdown"
        )


async def _get_date_and_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("Usage: /start 20250524 Interstella")
        return None

    date = args[0]
    title = " ".join(args[1:])
    print(f"Input date: {date}, title: {title}")
    return (date, title)


async def _fetch_and_display_movieinfo(context: ContextTypes.DEFAULT_TYPE):
    theater = context.job.data["theater"]
    title = context.job.data["title"]
    date = context.job.data["date"]

    try:
        # Fetch movie data
        theater.fetch_movies(date)
        movie = theater.get_movie(title)
        movie.display_movieinfo()
        movie.display_showtimes()
    except:
        print("error @ fetch_movies")

    try:
        # Movie or showtimes not found
        if not movie:
            await context.bot.send_message(
                chat_id=context.job.chat_id, text=f"Movie '{title}' not found"
            )
            return
        if len(movie.get_showtimes()) == 0:
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"No showtimes available for '{title}'",
            )
            return

        # Build message
        msg = movie.get_showtime_msg()
        await context.bot.send_message(
            chat_id=context.job.chat_id, text=msg, parse_mode="Markdown"
        )

    except KeyError as e:
        print(f"Missing key in job data")

    except Exception as e:
        print(f"Failed to send message")
