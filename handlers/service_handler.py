from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def register(app):
    app.add_handler(CommandHandler("debugjobs", debug_jobs))


async def debug_jobs(update: Update, context: CallbackContext) -> None:
    """
    Lists currently scheduled jobs (for debugging).
    """
    jobs = context.job_queue.jobs()

    if not jobs:
        await update.message.reply_text("🟡 Жодна задача не запланована.")
        return

    messages = []
    for job in jobs:
        next_run = job.next_t
        messages.append(
            f"🔧 <b>{job.name}</b>\n"
            f"➡️ Наступний запуск: <code>{next_run.strftime('%Y-%m-%d %H:%M:%S %Z')}</code>"
        )

    await update.message.reply_text("\n\n".join(messages), parse_mode="HTML")
