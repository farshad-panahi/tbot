# MARK:imports
import logging
from typing import Final
from uuid import uuid4
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import Application, ContextTypes, CommandHandler, InlineQueryHandler
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

    async def inline_query(
            update:Update,
            context:ContextTypes.DEFAULT_TYPE
    ):
        query = update.inline_query.query
        data = requests.get("https://thronesapi.com/api/v2/Characters")
        data = data.json()
        characters = {}
        for character in data:
            characters[character["fullName"]] = character["imageUrl"]
        if not query:
            results = []

            for name, url in characters.items():
                newItem = InlineQueryResultPhoto(
                    id=str(uuid4()),
                    photo_url=url,
                    thumbnail_url=url,
                    caption=name
                )
                results.append(newItem)
        else:
            results = []
            for name, url in characters.items():
                if query in name:
                    newItem = InlineQueryResultPhoto(
                        id=str(uuid4()), photo_url=url, thumbnail_url=url, caption=name
                    )
                    results.append(newItem)
        await update.inline_query.answer(results, auto_pagination=True)

    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(InlineQueryHandler(inline_query))
    bot.run_polling()

if __name__ == "__main__":
   main()
