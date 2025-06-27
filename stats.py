# ─ stats.py ─
"""
Keeps per-chat question counters and persists them to disk.
"""

import json
from collections import defaultdict
from typing import DefaultDict

from config import QUESTIONS_FILE

# chat_id -> user_id -> count
Counters = DefaultDict[int, DefaultDict[int, int]]
_counters: Counters = defaultdict(lambda: defaultdict(int))


def _load() -> None:
    if QUESTIONS_FILE.exists():
        try:
            data: dict[str, dict[str, int]] = json.loads(QUESTIONS_FILE.read_text("utf-8"))
            for chat, users in data.items():
                for uid, cnt in users.items():
                    _counters[int(chat)][int(uid)] = cnt
        except json.JSONDecodeError:
            pass


def _save() -> None:
    out = {str(c): {str(u): n for u, n in users.items()} for c, users in _counters.items()}
    QUESTIONS_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), "utf-8")


def increment(chat_id: int, user_id: int) -> None:
    """
    +1 to the user’s counter and save immediately.
    """
    _counters[chat_id][user_id] += 1
    _save()


def get_chat_counters(chat_id: int) -> dict[int, int]:
    """
    Returns a dict {user_id: count} for the given chat.
    """
    return _counters.get(chat_id, {})


# load once on import
_load()
