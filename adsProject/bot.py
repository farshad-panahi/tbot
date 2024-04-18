import os
from typing import Final

from bson import ObjectId
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    InlineQueryResultPhoto,
    MenuButton
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler,
    InlineQueryHandler,
)
from decouple import config
from mongo_client import AdsMongoClient

BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

CATEGORY, PHOTO, DESCRIPTION = range(3)
# db connection
db_client = AdsMongoClient("localhost", 27017)
dev_id = int(config("DEVELOPER_ID"))

async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="سلام، من ربات ثبت آگهی هستم. برای ثبت آگهی جدید از دستور  `/add_advertising` استفاده کنید.",
        reply_to_message_id=update.effective_message.id,
    )


async def add_category_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = int(update.effective_user.id)
    if dev_id != user_id:
      await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="شما اجازه دسترسی به این دستور را ندارید.",
        reply_to_message_id=update.effective_message.id,
    )

    elif user_id == dev_id:
        category = ' '.join([str(i) for i in context.args])
        db_client.add_category(category)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"دسته بندی {category} با موفقیت اضافه شد.",
            reply_to_message_id=update.effective_message.id
        )

async def remove_category_command_handler(update:Update, context:ContextTypes.DEFAULT_TYPE):
    category=' '.join(context.args)
    user_id = update.effective_user.id
    if user_id == dev_id:
        db_client.delete_category(category)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='deleted as you expected',
            reply_to_message_id=update.effective_message.id
        )


async def add_advertising_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    categories = db_client.get_categories()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = "لطفا از بین دسته بندی های زیر یکی را انتخاب کنید:\n"+"\n".join(categories),
        reply_to_message_id=update.effective_message.id
    )
    return CATEGORY

async def choice_category_message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data["category"] = str(update.effective_message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="لطفا عکس آگهی خود را ارسال کنید.",
        reply_to_message_id=update.effective_message.id
    )
    return PHOTO


async def photo_message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    context.user_data['photo_url'] = str(update.effective_message.photo[-1].file_id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="لطفا توضیحات آگهی خود را وارد کنید. در توضیحات می توانید اطلاعاتی مانند قیمت، شماره تماس و ... را وارد کنید.",
        reply_to_message_id=update.effective_message.id,
    )
    return DESCRIPTION

async def description_message_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    description = update.effective_message.text
    db_client.add_advertising(
        user_id=update.effective_user.id,
        photo_url=context.user_data['photo_url'],
        category=context.user_data['category'],
        description=description if description else ''
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="آگهی شما با موفقیت ثبت شد.",
        reply_to_message_id=update.effective_message.id
    )
    return ConversationHandler.END

async def cancel_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="عملیات ثبت آگهی لغو شد. برای ثبت آگهی جدید از دستور /add_category استفاده کنید.",
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END


async def my_ads_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ads = db_client.get_ads_by_user_id(update.effective_user.id)

    if len(ads) == 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="شما هیچ آگهی ثبت نکرده‌اید.",
            reply_to_message_id=update.effective_message.id
        )
    else:
        for ad in ads:
            await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=ad["photo_url"],
            caption=ad["description"] + f"\n\n" + "برای حذف آگهی از دستور زیر استفاده کنید."+"\n\n"+f"/delete_ad {ad['id']}",
            reply_to_message_id=update.effective_message.id,
        )

async def delete_ad_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ad_id = str(context.args[0])
    user_id = int(update.effective_user.id)

    db_client.delete_advertising(user_id, ad_id)
    await context.bot.send_message(
      chat_id=update.effective_chat.id, 
      text="آگهی با موفقیت حذف شد.",
      reply_to_message_id=update.effective_message.id
      )


async def search_ads_by_category_inline_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.inline_query.query
    ads = db_client.get_ads_by_category(query)
    results = [
        InlineQueryResultPhoto(
            id=ad["id"],
            title=ad["description"],
            photo_url=ad["photo_url"],
            thumbnail_url=ad["photo_url"],
            caption=ad["description"],
        )
        for ad in ads
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command_handler))
    app.add_handler(CommandHandler("add_category", add_category_command_handler))
    app.add_handler(CommandHandler("my_ads", my_ads_command_handler))
    app.add_handler(CommandHandler("delete_ad", delete_ad_command_handler))
    app.add_handler(InlineQueryHandler(search_ads_by_category_inline_query))
    app.add_handler(CommandHandler("remove", remove_category_command_handler))

    app.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("add_advertising", add_advertising_command_handler)
            ],
            states={
                CATEGORY: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, choice_category_message_handler
                    )
                ],
                PHOTO: [
                    MessageHandler(filters.PHOTO, photo_message_handler),
                ],
                DESCRIPTION: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, description_message_handler
                    )
                ],
            },
            fallbacks=[
                CommandHandler("cancel", cancel_command_handler),
            ],
            allow_reentry=True,
        )
    )
    app.run_polling()
