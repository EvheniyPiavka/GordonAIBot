import re


def ends_with_question_no_space(text: str) -> bool:
    """
    Checks if the text ends with a question mark without a space before it.

    Examples:
        "Is it true?"     -> True
        "Is it true ?"    -> False

    Args:
        text (str): The input message text.

    Returns:
        bool: True if it ends with '?' and no space before it.
    """
    return bool(re.search(r"[^ ]\?$", text))


def next_answer_id(answers: list[dict]) -> int:
    """
    Returns the next available ID for a new answer.

    Args:
        answers (list[dict]): The current list of answer objects.

    Returns:
        int: A unique integer ID (incremental).
    """
    return max((q["id"] for q in answers), default=0) + 1


def medal_for_rank(rank: int) -> str:
    """
    Maps 1,2,3 → 🥇🥈🥉; others → empty string.
    """
    return {1: "🥇 ", 2: "🥈 ", 3: "🥉 "}.get(rank, "")
