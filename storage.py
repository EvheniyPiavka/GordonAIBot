import json

from config import ANSWERS_FILE, SUBSCRIPTIONS_FILE


def _load(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ===== answers =====
def get_answers() -> list[dict]:
    return _load(ANSWERS_FILE, [])


def save_answers(data: list[dict]) -> None:
    _save(ANSWERS_FILE, data)


# ===== subscriptions =====
def get_subscriptions() -> set[int]:
    return set(_load(SUBSCRIPTIONS_FILE, []))


def save_subscriptions(ids: set[int]) -> None:
    _save(SUBSCRIPTIONS_FILE, list(ids))
