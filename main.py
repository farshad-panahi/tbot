import pymongo
from decouple import config

from typing import Final
from decouple import config
from telegram import (
    Update,
)
from pprint import pprint
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

from mongo_client import ExpenseMongoClient

db_client = ExpenseMongoClient("localhost", 27017)

BOT_TOKEN: Final = config("TELEGRAM_API_TOKEN")


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def add_expense_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    amount, category, description = context.args[0], context.args[1], context.args[2:]
    db_client.add_expense(
        user_id=str(update.effective_user.id),
        amount=int(amount),
        category=category,
        description=" ".join(description),
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Expense added successfully!",
        reply_to_message_id=update.effective_message.id,
    )


async def get_expenses_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    expenses = db_client.get_expenses(user_id)
    categories = db_client.get_categories(user_id)
    if len(context.args) == 0:
        text = "Your expenses are:\n"
        for expense in expenses:
            text += f"{expense['amount']} - {expense['category']} - {expense['description']}\n"

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_to_message_id=update.effective_message.id,
        )
    elif len(context.args) > 0:

        text = "Your expenses are:\n"
        for expense in expenses:
            if expense["category"] in context.args[0]:
                text += f"{expense['amount']} - {expense['category']} - {expense['description']}\n"

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            reply_to_message_id=update.effective_message.id,
        )


async def get_categories_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user_id = update.effective_user.id
    categories = db_client.get_categories(user_id)
    text = f"Your categories are: {', '.join(categories)}"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


async def get_total_expense_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user.id
    total = db_client.get_total_expense(user)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your total expense is: {int(total)}",
        reply_to_message_id=update.effective_message.id,
    )


async def get_total_expense_by_category_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    total_expense = db_client.get_total_expense_by_category(user_id)
    text = "Your total expenses by category are:\n"
    for category, expense in total_expense.items():
        text += f"{category}: {expense}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_to_message_id=update.effective_message.id,
    )


if __name__ == "__main__":
    expense_mongo_client = ExpenseMongoClient("localhost", 27017)
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(CommandHandler("add_expense", add_expense_command_handler))
    bot.add_handler(CommandHandler("get_expenses", get_expenses_command_handler))
    bot.add_handler(CommandHandler("get_categories", get_categories_command_handler))
    bot.add_handler(CommandHandler("get_total", get_total_expense_command_handler))
    bot.add_handler(CommandHandler("get_total_by_category", get_total_expense_by_category_command_handler))

    bot.run_polling()
