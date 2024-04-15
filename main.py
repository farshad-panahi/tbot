import logging
from typing import Final
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from decouple import config


TOKEN: Final = config("TELEGRAM_API_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def say_hello(context:ContextTypes.DEFAULT_TYPE):
  job = context.job
  await context.bot.send_message(
    text='Hello',
    chat_id=job.chat_id
  )

async def say_hello_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  a = int(context.args[0])
  if a < 5:
    await context.bot.send_message(
      chat_id=update.effective_chat.id,
      text='please enter a number greater than 5'
    )
    return
  job_name = str(update.effective_chat.id)
  context.job_queue.run_repeating(
    say_hello,
    chat_id=update.effective_chat.id,
    interval=a,
    name=job_name,
  )
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='ok!'
  )

async def unset_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
  job = context.job_queue.get_jobs_by_name(str(update.effective_chat.id))
  for n in job:
    n.schedule_removal()

  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='job removed'
  )


if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()
    application.add_handler("hello", say_hello_handler)
    application.add_handler("unset", unset_handler)

    application.run_polling()
