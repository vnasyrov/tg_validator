import io
import json
import os

from telebot import TeleBot

bot = TeleBot(os.environ["BOT_TOKEN"])


@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.reply_to(
        message,
        "Отправьте JSON текстом — проверю синтаксис "
        "и верну отформатированный результат.",
    )


@bot.message_handler(content_types=["text"])
def validate_json(message):
    try:
        payload = json.loads(message.text)
    except json.JSONDecodeError as error:
        bot.reply_to(
            message,
            f"Ошибка JSON: {error.msg}\n"
            f"Строка {error.lineno}, столбец {error.colno}.",
        )
        return

    formatted = json.dumps(
        payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )

    # Большие результаты отправляем файлом.
    if len(formatted.encode("utf-8")) > 3500:
        document = io.BytesIO(formatted.encode("utf-8"))
        document.name = "formatted.json"
        bot.send_document(
            message.chat.id,
            document,
            caption="JSON корректен.",
        )
    else:
        bot.reply_to(message, f"JSON корректен:\n\n{formatted}")


if __name__ == "__main__":
    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=30,
        allowed_updates=["message"],
    )
