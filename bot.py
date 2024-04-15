import logging
from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, ContextTypes, InlineQueryHandler


async def inlineHandle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_request = update.inline_query
    if not inline_request:
        return

    query = inline_request.query
    if not query:
        return

    responses = [
        InlineQueryResultArticle(
            id="1",
            title="UpperCase",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id="2",
            title="LowerCase",
            input_message_content=InputTextMessageContent(query.lower()),
        ),
    ]

    await inline_request.answer(responses)

# job queue
async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(
        job.chat_id, text=f"Beep! {job.data} seconds are over!"
    )


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    due = float(context.args[0])
    context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)


if __name__ == "__main__":
    token = config("TELEGRAM_API_TOKEN")
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.add_handler(InlineQueryHandler(inlineHandle))
    application.add_handler(CommandHandler("set", set_timer))
    application.run_polling()
