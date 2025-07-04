from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)
from config import BOT_TOKEN, AUTHORIZED_USERS
from task_extraction import extract_tasks_from_message
from sheets_manager import (
    append_task_to_sheet,
    get_spreadsheet_url,
    get_all_worksheets,
    get_worksheet_summary,
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process incoming messages and ask Yes/No to create task"""
    message = update.message
    if not message or not message.from_user:
        return

    user = message.from_user
    chat = message.chat

    is_authorized = user.id in AUTHORIZED_USERS
    if not is_authorized:
        return

    text = message.text
    if not text:
        return

    if chat.type == "private":
        chat_name = f"Private_{user.username or user.first_name}"
    else:
        chat_name = chat.title

    tasks = extract_tasks_from_message(text)
    if tasks:
        for task in tasks:
            # Store info temporarily in context to handle later
            context.user_data["pending_task"] = {
                "task": task,
                "full_message": text,
                "chat_name": chat_name,
                "from_user": user.full_name,
            }

            keyboard = [
                [
                    InlineKeyboardButton("✅ Yes", callback_data="create_task_yes"),
                    InlineKeyboardButton("❌ No", callback_data="create_task_no"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await message.reply_text(
                f"Do you want to create this task?\n\n➡️ *{task}*",
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )


async def handle_task_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Yes/No button presses"""
    query = update.callback_query
    await query.answer()

    user_data = context.user_data.get("pending_task")
    if not user_data:
        await query.edit_message_text("No task pending.")
        return

    answer = "Yes" if query.data == "create_task_yes" else "No"

    success = append_task_to_sheet(
        user_data["task"],
        user_data["from_user"],
        user_data["full_message"],
        user_data["chat_name"],
        answer
    )

    if success:
        await query.edit_message_text(f"✅ Task processed and marked as '{answer}'.")
    else:
        await query.edit_message_text("❌ Failed to save the task.")

    # Clear pending
    context.user_data["pending_task"] = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Send me a message starting with # and I'll ask if you want to save it as a task."
    )


async def sheet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheet_url = get_spreadsheet_url()
    if sheet_url:
        await update.message.reply_text(f"📊 Here's the task list: {sheet_url}")
    else:
        await update.message.reply_text("❌ Unable to retrieve the sheet link.")


async def tabs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tabs = get_all_worksheets()
    if tabs:
        message = "📊 Available task lists:\n\n"
        for i, tab in enumerate(tabs, 1):
            message += f"{i}. {tab}\n"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("No task lists created yet.")


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    summary = get_worksheet_summary()
    if summary:
        message = "📈 Task Summary:\n\n"
        total_tasks = 0
        for tab, count in summary.items():
            total_tasks += count
            message += f"{tab}: {count} tasks\n"
        message += f"\nTotal: {total_tasks} tasks"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("No task lists created yet.")


def create_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("sheet", sheet_command))
    app.add_handler(CommandHandler("tabs", tabs_command))
    app.add_handler(CommandHandler("summary", summary_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_task_confirmation))

    commands = [
        BotCommand("start", "Start the bot and get help"),
        BotCommand("sheet", "Get the Google Sheet URL"),
        BotCommand("tabs", "List all tabs"),
        BotCommand("summary", "Show task summary"),
    ]

    async def setup_hook(self):
        await self.bot.set_my_commands(commands)

    app.post_init = setup_hook

    return app
