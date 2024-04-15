# MARK:imports
import logging
from typing import Final
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from decouple import config
from datetime import datetime as dt

def main():
    TOKEN: Final = config("TELEGRAM_API_TOKEN")

    logging.basicConfig(
      format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
      level=logging.INFO
  )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logger = logging.getLogger(__name__)

    async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hello, I'm a bot! Thanks for using me!",
        )

    async def repeat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        words = " ".join(context.args)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{words}",
        )

    async def time_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        time = dt.now().strftime("%Y-%m-%d %H:%M")

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{time}",
        )
    async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{HELP_COMMAND_RESPONSE}",
        )
    async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
          chat_id=update.effective_chat.id, text=update.message.text
      )
        await context.bot.send_message(
          chat_id=update.effective_chat.id,
          text=f"repeated {update.effective_user.first_name}!",
      )

    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()
    # Command Handler
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("repeat", repeat_handler))
    application.add_handler(CommandHandler("time", time_handler))
    application.add_handler(CommandHandler("help", time_handler))

    # Message Handler
    application.add_handler(MessageHandler(filters.TEXT, echo_handler))
    # Run the Bot
    application.run_polling()

if __name__ == "__main__":
   main()
