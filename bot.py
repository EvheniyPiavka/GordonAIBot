from telegram.ext import Application

import jobs
from commands import setup_commands
from config import TOKEN
from handlers import text_handler, answers_handler, subscription_handler, service_handler, surveys_handler, \
    rankings_handler


def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(jobs.setup)
        .post_init(setup_commands)
        .build()
    )

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
