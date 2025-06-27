from datetime import datetime, timedelta

from telegram.ext import Application

from storage import get_subscriptions


async def daily_message(ctx):
    for chat_id in get_subscriptions():
        await ctx.bot.send_message(chat_id, text="19:10")


async def setup(app: Application):
    now = datetime.now().astimezone()
    first = now.replace(hour=19, minute=11, second=0, microsecond=0)
    if now >= first:
        first += timedelta(days=1)

    app.job_queue.run_repeating(
        daily_message,
        interval=timedelta(days=1),
        first=first,
        job_kwargs={"misfire_grace_time": 30},
        name="daily_message"
    )
