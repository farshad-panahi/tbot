from datetime import datetime
from typing import Final


from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime
from decouple import config


BOT_TOKEN: Final = config("TELEGRAM_API_TOKEN")

async def say_hello(context:ContextTypes.DEFAULT_TYPE):
  job = context.job
  await context.bot.send_message(
    text='HI',
    chat_id=job.chat_id
  )

async def say_hello_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    a = int(context.args[0])
    if a < 5:
        await context.bot.send_message(
          chat_id=update.effective_chat.id,
          text="must be greater than 5!",
          reply_to_message_id=update.effective_message.id,
      )
        return
    this_job = str(update.effective_chat.id)
    context.job_queue.run_repeating(
       say_hello, # callback function
       chat_id=update.effective_chat.id,
       interval=a,
       name=this_job, # job name
       )
    await context.bot.send_message(
       chat_id=update.effective_chat.id,
       text='its set'
    )
async def unset_handler(
      update:Update,
      context:ContextTypes.DEFAULT_TYPE,
):
  running_jobs = context.job_queue.get_jobs_by_name(str(update.effective_chat.id))
  for n in running_jobs:
      n.schedule_removal()
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text='job removed'
  )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("hello", say_hello_handler))
    bot.add_handler(CommandHandler("remove", unset_handler))

    bot.run_polling()

