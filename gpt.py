from openai import OpenAI

from config import OPENAI_API_KEY, GPT_MODEL, GPT_TEMP, MAX_HISTORY_LEN

client = OpenAI(api_key=OPENAI_API_KEY)
_histories: dict[int, list[dict]] = {}


async def ask_chatgpt_with_history(update, ctx):
    cid, prompt = update.message.chat_id, update.message.text.partition(" ")[2]
    hist = _histories.setdefault(cid, [])
    hist.append({"role": "user", "content": prompt})

    try:
        res = client.chat.completions.create(
            model=GPT_MODEL, messages=hist, temperature=GPT_TEMP
        )
        reply = res.choices[0].message.content.strip()
    except Exception:
        reply = "🥴 Я шось не викупив..."

    hist.append({"role": "assistant", "content": reply})
    if len(hist) > MAX_HISTORY_LEN:
        _histories[cid] = hist[-MAX_HISTORY_LEN:]

    await update.message.reply_text(reply, reply_to_message_id=update.message.message_id)
