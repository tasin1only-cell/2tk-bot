import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

PRIVACY_URL = "https://tasin1only-cell.github.io/2tk-privacy/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📱 Services", callback_data="services"),
            InlineKeyboardButton("💰 Balance", callback_data="balance"),
        ],
        [
            InlineKeyboardButton("📦 Orders", callback_data="orders"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton("🔒 Privacy Policy", url=PRIVACY_URL),
        ],
    ]

    await update.message.reply_text(
        "💎 *2TK OTP Numbers Bot* 🤖\n\n"
        "Welcome! 👋\n\n"
        "⚡ Fast • Simple • Automated\n"
        "💰 Services from ৳2\n\n"
        "👇 Select an option:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 *Your Balance*\n\n"
        "Current balance: ৳0.00\n\n"
        "This is the demo balance system.",
        parse_mode="Markdown",
    )


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 *Your Orders*\n\n"
        "You don't have any orders yet.",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ *Help Center*\n\n"
        "/start — Open main menu\n"
        "/menu — Open main menu\n"
        "/balance — Check balance\n"
        "/orders — View orders\n"
        "/help — Help center\n"
        "/privacy — Privacy Policy\n\n"
        "For support, contact the bot operator through the available support channel.",
        parse_mode="Markdown",
    )


async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔒 Privacy Policy\n\n{PRIVACY_URL}"
    )


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 *Support*\n\n"
        "Please contact the bot operator through the official support channel.",
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        await query.message.reply_text(
            "📱 *Services*\n\n"
            "Demo service menu is currently active.\n\n"
            "Real verification-number/provider integration is not enabled.",
            parse_mode="Markdown",
        )

    elif query.data == "balance":
        await query.message.reply_text(
            "💰 *Balance*\n\n"
            "Current balance: ৳0.00",
            parse_mode="Markdown",
        )

    elif query.data == "orders":
        await query.message.reply_text(
            "📦 *Orders*\n\n"
            "No orders found.",
            parse_mode="Markdown",
        )

    elif query.data == "help":
        await help_command(update, context)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("orders", orders))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("privacy", privacy))
    application.add_handler(CommandHandler("support", support))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("2TK Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
