from omdb import OMDBClient
from decouple import config

from typing import Final
from decouple import config
from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
)
from pprint import pprint
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    InlineQueryHandler,
)


BOT_TOKEN: Final = config("TELEGRAM_API_TOKEN")
OMDB_API_KEY = config("ACTIVATE_CODE")

client = OMDBClient(apikey=OMDB_API_KEY)


class Movie(object):
    def __init__(
        self,
        title: str = "",
        year: str = "",
        imdb_id: str = "",
        type: str = "",
        poster: str = "",
    ):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.type = type
        self.poster = poster

    def from_dict(self, movie: dict):
        self.title = movie["title"]
        self.year = movie["year"]
        self.imdb_id = movie["imdb_id"]
        self.type = movie["type"]
        self.poster = movie["poster"]
        return self


def search_movie_by_title(title: str) -> list[Movie]:
    results = client.search(title, media_type="movie")
    movies = []
    for movie in results:
        movie = Movie().from_dict(movie)
        movies.append(movie)
    return movies


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def search_movie_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if query.split(" ")[-1] == "only_poster":
        query = " ".join(query.split(" ")[0:-1])
        movies = search_movie_by_title(query)
        print(query)
        results = [
            InlineQueryResultPhoto(
                id=movie.imdb_id,
                caption=f"{movie.title} - {movie.year}",
                title=movie.title,
                thumbnail_url=movie.poster,
                photo_url=movie.poster,
            )
            for movie in movies
        ]
        # await update.inline_query.answer(results, auto_pagination=True)
        await context.bot.answer_inline_query(
            inline_query_id=update.inline_query.id,
            results=results,
        )

    if query and query.split(" ")[-1] != "only_poster":
        movies = search_movie_by_title(query)
        results = [
            InlineQueryResultArticle(
                id=movie.imdb_id,
                title=movie.title,
                input_message_content=InputTextMessageContent(
                    message_text=f"{movie.title} - {movie.year}:\n\nhttps://www.imdb.com/title/{movie.imdb_id}/"
                ),
                thumbnail_url=movie.poster,
            )
            for movie in movies
        ]
        # await update.inline_query.answer(results, auto_pagination=True)
        await context.bot.answer_inline_query(
            inline_query_id=update.inline_query.id,
            results=results,
        )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(InlineQueryHandler(search_movie_inline_query))

    bot.run_polling()
