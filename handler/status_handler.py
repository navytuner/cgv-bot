from telegram import Update
from telegram.ext import ContextTypes
from config.settings import INTERVAL


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Get all jobs
    all_jobs = context.job_queue.jobs()
    chat_jobs = [job for job in all_jobs if job.chat_id == chat_id]

    if not chat_jobs:
        await update.message.reply_text(
            "**No active monitoring**\n\n"
            "Use `/start YYYY.MM.DD Movietitle` to begin monitoring",
            parse_mode="Markdown",
        )
        return

    msg = f"📊 **Active Monitoring ({len(chat_jobs)} job{'s' if len(chat_jobs) != 1 else ''})**\n\n"
    for i, job in enumerate(chat_jobs, 1):
        job_data = job.data or {}
        title = job_data.get("title", "Unknown")
        theater = job_data.get("theater")
        date_str = theater.get_date().strftime("%Y.%m.%d") if theater else "Unknown"

        msg += f"{i}. **{title}**\n"
        msg += f"   📅 Date: {date_str}\n"
        msg += f"   ⏱️ Interval: {INTERVAL}s\n\n"

    msg += "Use `/stop` to stop all monitoring."

    await update.message.reply_text(msg, parse_mode="Markdown")
