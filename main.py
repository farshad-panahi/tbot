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

    async def fact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hello, I'm a bot! Thanks for using me!",
        )
    async def fact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        data = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
        fact = data.json()["text"]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=fact)

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("fact", fact_handler))

    application.run_polling()

if __name__ == "__main__":
   main()
