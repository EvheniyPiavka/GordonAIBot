# ─ handlers/rankings_handler.py ─
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from stats import get_chat_counters
from utils import medal_for_rank


def register(app):
    app.add_handler(CommandHandler("rankings", show_rankings))
    app.add_handler(CommandHandler("myrank", show_myrank))


async def show_rankings(update: Update, context: CallbackContext) -> None:
    """
    Sends the top 10 askers for the current chat.
    """
    chat_id = update.effective_chat.id
    counts = get_chat_counters(chat_id)
    if not counts:
        await update.message.reply_text("❌ Ніхто нічого не питав. І правильно.")
        return

    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:10]
    lines = ["🏆 Топ довбойобів:"]
    for pos, (uid, cnt) in enumerate(top, 1):
        # try to fetch username; fall back to 'User <id>'
        try:
            user_obj = await context.bot.get_chat_member(chat_id, uid)
            name = f"@{user_obj.user.username}" if user_obj.user.username else user_obj.user.full_name
        except Exception:
            name = f"User {uid}"
        medal = medal_for_rank(pos)
        lines.append(f"{medal}{pos}. {name} — {cnt}")

    await update.message.reply_text("\n".join(lines))


async def show_myrank(update: Update, context: CallbackContext) -> None:
    """
    Shows the requesting user their rank & question count.
    """
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    counts = get_chat_counters(chat_id)
    if not counts or user_id not in counts:
        await update.message.reply_text("Красава! 😶 Ти ще нічого не питав.")
        return

    sorted_users = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    position = next(i for i, (uid, _) in enumerate(sorted_users, 1) if uid == user_id)
    total = counts[user_id]
    medal = medal_for_rank(position)
    await update.message.reply_text(
        f"{medal}Твоя позиція в рейтингу: {position}\n"
        f"Ти поставив {total} питань."
    )
