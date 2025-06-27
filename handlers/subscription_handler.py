from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from storage import get_subscriptions, save_subscriptions

subscribed_chats: set[int] = get_subscriptions()


def register(app):
    app.add_handler(CommandHandler("startdaily", start_daily))
    app.add_handler(CommandHandler("stopdaily", stop_daily))


async def start_daily(update: Update, context: CallbackContext) -> None:
    """
    Subscribes the chat to daily messages at 19:10.
    """
    chat_id = update.message.chat_id
    if chat_id not in subscribed_chats:
        subscribed_chats.add(chat_id)
        save_subscriptions(subscribed_chats)
        await update.message.reply_text("✅ Активую підписку на 19:10")
    else:
        await update.message.reply_text("Підписка уже активна, іди нахуй!")


async def stop_daily(update: Update, context: CallbackContext) -> None:
    """
    Unsubscribes the chat from daily messages.
    """
    chat_id = update.message.chat_id
    if chat_id in subscribed_chats:
        subscribed_chats.remove(chat_id)
        save_subscriptions(subscribed_chats)
        await update.message.reply_text("❌ Підписка скасована.")
    else:
        await update.message.reply_text("You're not subscribed. Don't mess around.")
