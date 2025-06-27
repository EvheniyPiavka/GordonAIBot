from telegram.ext import Application

import jobs
from config import TOKEN
from handlers import text_handler, answers_handler, subscription_handler, service_handler, surveys_handler, \
    rankings_handler


def main():
    app = Application.builder().token(TOKEN).post_init(jobs.setup).build()

    for module in (text_handler,
                   answers_handler,
                   subscription_handler,
                   service_handler,
                   surveys_handler,
                   rankings_handler):
        module.register(app)

    app.run_polling(allowed_updates="all")


if __name__ == "__main__":
    main()
