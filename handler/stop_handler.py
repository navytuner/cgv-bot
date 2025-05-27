from telegram import Update
from telegram.ext import ContextTypes


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if not jobs:
        await update.message.reply_text("No active job to stop")
        return
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text("Stopped successfully")
