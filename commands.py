# commands.py
"""
Sets different slash-command menus for private chats and group chats.
Call setup_commands(app) once after the bot is built.
"""

from telegram import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    BotCommandScopeDefault,
)
from telegram.ext import Application


async def setup_commands(app: Application) -> None:
    # ----- 1. Private (DM) menu ----- #
    private_commands = [
        BotCommand("help",        "Показати список можливостей"),
        BotCommand("startdaily",  "Увімкнути щоденне нагадування"),
        BotCommand("stopdaily",   "Вимкнути щоденне нагадування"),
        BotCommand("listanswers", "Список випадкових фраз"),
        BotCommand("addanswer",   "Додати фразу"),
        BotCommand("delanswer",   "Видалити фразу"),
        BotCommand("rankings",    "Топ довбойобів"),
        BotCommand("myrank",      "Твоя позиція"),
    ]
    await app.bot.set_my_commands(
        commands=private_commands,
        scope=BotCommandScopeAllPrivateChats(),
    )

    # ----- 2. Group menu ----- #
    group_commands = [
        BotCommand("play",      "Голосування: граємо?"),
        BotCommand("rankings",  "Топ довбойобів"),
        BotCommand("myrank",    "Твоя позиція"),
    ]
    await app.bot.set_my_commands(
        commands=group_commands,
        scope=BotCommandScopeAllGroupChats(),
    )

    # (optional) clear default scope to avoid duplicates in clients
    await app.bot.set_my_commands(
        commands=[],
        scope=BotCommandScopeDefault(),
    )
