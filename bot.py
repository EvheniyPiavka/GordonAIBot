from telegram.ext import Application

import jobs
from config import TOKEN
from handlers import text, answers, subs, service, surveys


def main():
    app = Application.builder().token(TOKEN).post_init(jobs.setup).build()

    for module in (text, answers, subs, service, surveys):
        module.register(app)

    app.run_polling(allowed_updates="all")


if __name__ == "__main__":
    main()
