# MARK:imports
import logging
from typing import Final
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from decouple import config
import requests

def main():
    TOKEN: Final = config("TELEGRAM_API_TOKEN")

    logging.basicConfig(
      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
      level=logging.INFO
  )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    async def add_c_handler(
            update:Update,
            context:ContextTypes.DEFAULT_TYPE
    ):
        m, n = int(context.args[0]), int(context.args[1])

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{n} + {m} = {n + m}"
        )

    async def mult_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        n, m = int(context.args[0]), int(context.args[1])

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{n} + {m} = {n * m}"
        )

    async def ex_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        exp = context.args
        resp = " ".join(i for i in exp)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{resp} = {eval(resp)}",
            reply_to_message_id=update.effective_message.id
        )

    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("add", add_c_handler))
    bot.add_handler(CommandHandler("mult", mult_handler))
    bot.add_handler(CommandHandler("ex", ex_handler))
    bot.run_polling()

if __name__ == "__main__":
   main()
