from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def register(app):
    app.add_handler(CommandHandler("play", survey))


async def survey(update: Update, context: CallbackContext) -> None:
    """
    Sends a non-anonymous poll to the group.
    """
    question = "Шо ви хлопчики горобчики? Гамаєм сьогодні?"
    options = [
        "Я реді сосати член 🍆",
        "Так",
        "Нема білетіків",
        "Буду в 10",
        "Я довбойоб і сьогодні пасую"
    ]
    await context.bot.send_poll(
        chat_id=update.message.chat_id,
        question=question,
        options=options,
        is_anonymous=False
    )
