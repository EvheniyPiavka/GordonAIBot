import random

from telegram import Update
from telegram.constants import MessageEntityType
from telegram.ext import CallbackContext, MessageHandler, filters

from gpt import ask_chatgpt_with_history
from storage import get_answers
from utils import ends_with_question_no_space

answers = get_answers()


def register(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))


async def handle_text(update: Update, context: CallbackContext):
    txt = update.message.text

    if _is_mentioned(update, context):
        await ask_chatgpt_with_history(update, context)
    elif ends_with_question_no_space(txt):
        await update.message.reply_text(random.choice(answers)["text"])


def _is_mentioned(update: Update, ctx) -> bool:
    ent = update.message.entities or []
    return any(
        e.type == MessageEntityType.MENTION and
        update.message.text[e.offset:e.offset + e.length] == f"@{ctx.bot.username}"
        for e in ent
    )
