import random
import re
import json
import openai
from datetime import time, datetime, timedelta

from openai import OpenAI
from telegram import Update
from telegram.constants import MessageEntityType
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext, JobQueue


SUBSCRIPTIONS_FILE = "subscriptions.json"
ANSWERS_FILE = "answers.json"

chat_histories = {}  # {chat_id: List[Dict[str, str]]}
MAX_HISTORY_LENGTH = 10
openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

def load_subscribed_chats():
    try:
        with open(SUBSCRIPTIONS_FILE, "r") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_subscribed_chats():
    with open(SUBSCRIPTIONS_FILE, "w") as file:
        json.dump(list(subscribed_chats), file)

subscribed_chats = load_subscribed_chats()

def load_answers() -> list[dict]:
    try:
        with open(ANSWERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_answers(data: list[dict]) -> None:
    with open(ANSWERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

answers: list[dict] = load_answers()

def next_quote_id() -> int:
    return max((q["id"] for q in answers), default=0) + 1

def ends_with_question_no_space(text):
    return bool(re.search(r'[^ ]\?$', text))

def is_mentioned(update: Update, context: CallbackContext) -> bool:
    text = update.message.text
    entities = update.message.entities or []
    return any(
        entity.type == MessageEntityType.MENTION and
        text[entity.offset:entity.offset + entity.length] == f"@{context.bot.username}"
        for entity in entities
    )



async def handle_text_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if is_mentioned(update, context):
        await respond_with_gpt(update, context)
    elif ends_with_question_no_space(text):
        response = random.choice(answers)["text"]
        await update.message.reply_text(response)

async def daily_message(context: CallbackContext) -> None:
    print("start sending daily message")
    for chat_id in subscribed_chats:
        await context.bot.send_message(chat_id=chat_id, text="19:10")

async def start_daily(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id not in subscribed_chats:
        subscribed_chats.add(chat_id)
        save_subscribed_chats()
        await update.message.reply_text("Активую підписку на 19:10")
    else:
        await update.message.reply_text("Підписка уже активна, іди нахуй!")

# Команда для остановки ежедневных сообщений
async def stop_daily(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id in subscribed_chats:
        subscribed_chats.remove(chat_id)
        save_subscribed_chats()
        await update.message.reply_text("Підписка скасована")
    else:
        await update.message.reply_text("Підписка не активна, не вийобуйся!")

async def debug_jobs(update: Update, context: CallbackContext) -> None:
    job_queue = context.job_queue
    jobs = job_queue.jobs()

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

async def list_answers(update: Update, _: CallbackContext) -> None:
    if not answers:
        await update.message.reply_text("Список порожній 🚫")
        return
    text = "\n".join(f"{q['id']}. {q['text']}" for q in answers)
    await update.message.reply_text(text)

async def add_answer(update: Update, _: CallbackContext) -> None:
    new_text = update.message.text.partition(" ")[2].strip()
    if not new_text:
        await update.message.reply_text(
            "Пришли фразу після команди, напр.: `/addanswer Привіт!`",
            parse_mode="Markdown"
        )
        return
    answer = {"id": next_quote_id(), "text": new_text}
    answers.append(answer)
    save_answers(answers)
    await update.message.reply_text(f"✅ Додано (ID {answer['id']}): «{answer['text']}»")

async def del_answer(update: Update, _: CallbackContext) -> None:
    arg = update.message.text.partition(" ")[2].strip()
    if not arg.isdigit():
        await update.message.reply_text(
            "Вкажи ID із `/listanswers`, напр.: `/delanswer 7`",
            parse_mode="Markdown"
        )
        return
    qid = int(arg)
    for q in answers:
        if q["id"] == qid:
            answers.remove(q)
            save_answers(answers)
            await update.message.reply_text(f"🗑 Видалено: «{q['text']}»")
            break
    else:
        await update.message.reply_text("Такого ID нема 🤷")

async def ask_chatgpt_with_history(chat_id: int, prompt: str) -> str:
    history = chat_histories.get(chat_id, [])
    history.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()

        # Добавим ответ бота в историю
        history.append({"role": "assistant", "content": reply})

        # Обрезаем, если слишком длинная
        if len(history) > MAX_HISTORY_LENGTH:
            history = history[-MAX_HISTORY_LENGTH:]

        chat_histories[chat_id] = history

        return reply
    except Exception as e:
        print(f"GPT error: {e}")
        return "🥴 Я шось не викупив..."


async def survey(update: Update, context: CallbackContext) -> None:
    question = "Шо ви хлопчики горобчики? Гамаєм сьогодні?"
    options = [
        "Я реді сосати член",
        "Так",
        "Нема білетіків",
        "Буду в 10",
        "Я довбойоб і сьогодні пасую"
    ]
    await context.bot.send_poll(chat_id=update.message.chat_id, question=question, options=options, is_anonymous=False)

async def respond_with_gpt(update: Update, context: CallbackContext) -> None:
    message = update.message
    text = message.text
    username = context.bot.username

    mentioned = any(
        entity.type == MessageEntityType.MENTION and
        text[entity.offset:entity.offset + entity.length] == f"@{username}"
        for entity in (message.entities or [])
    )

    if not mentioned:
        return

    cleaned_text = text.replace(f"@{username}", "").strip()
    if not cleaned_text:
        await message.reply_text("🤖 А шо ти хочеш?", reply_to_message_id=message.message_id)
        return

    reply = await ask_chatgpt_with_history(message.chat_id, cleaned_text)
    await message.reply_text(reply, reply_to_message_id=message.message_id)

async def setup_jobs(app: Application) -> None:
    job_queue = app.job_queue

    now = datetime.now().astimezone()
    first_run = now.replace(hour=19, minute=11, second=0, microsecond=0)

    if now >= first_run:
        first_run += timedelta(days=1)

    job_queue.run_repeating(
        callback=daily_message,
        interval=timedelta(days=1),
        first=first_run,
        job_kwargs={"misfire_grace_time": 30}
    )

    print(f"✅ Scheduled daily_message for {first_run.isoformat()}")


def main():
    TOKEN = "7848960140:AAFdDLDKaN2p5k3t2GfUgMaGL9mXo32VCL4"
    app = Application.builder().token(TOKEN).post_init(setup_jobs).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    app.add_handler(CommandHandler("startdaily", start_daily))
    app.add_handler(CommandHandler("stopdaily", stop_daily))
    app.add_handler(CommandHandler("debugjobs", debug_jobs))
    app.add_handler(CommandHandler("play", survey))

    app.add_handler(CommandHandler("listanswers", list_answers))
    app.add_handler(CommandHandler("addanswer", add_answer))
    app.add_handler(CommandHandler("delanswer", del_answer))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
