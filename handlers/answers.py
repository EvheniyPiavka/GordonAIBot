from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from storage import get_answers, save_answers
from utils import next_quote_id

answers = get_answers()


def register(app):
    app.add_handler(CommandHandler("listanswers", list_answers))
    app.add_handler(CommandHandler("addanswer", add_answer))
    app.add_handler(CommandHandler("delanswer", del_answer))


async def list_answers(update: Update, _: CallbackContext):
    if not answers:
        await update.message.reply_text("Список порожній 🚫")
        return
    await update.message.reply_text(
        "\n".join(f"{q['id']}. {q['text']}" for q in answers)
    )


async def add_answer(update: Update, _: CallbackContext):
    text = update.message.text.partition(" ")[2].strip()
    if not text:
        await update.message.reply_text("Використання: /addanswer <фраза>")
        return
    q = {"id": next_quote_id(answers), "text": text}
    answers.append(q);
    save_answers(answers)
    await update.message.reply_text(f"✅ Додано ID {q['id']}")


async def del_answer(update: Update, _: CallbackContext):
    arg = update.message.text.partition(" ")[2].strip()
    if not arg.isdigit():
        await update.message.reply_text("Використання: /delanswer <ID>")
        return
    qid = int(arg)
    for q in answers:
        if q["id"] == qid:
            answers.remove(q);
            save_answers(answers)
            await update.message.reply_text("🗑 Видалено")
            return
    await update.message.reply_text("Такого ID нема 🤷")
