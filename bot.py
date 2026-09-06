import os
import sqlite3
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PRIVACY_URL = "https://tasin1only-cell.github.io/2tk-privacy/"
DB_FILE = "bot.db"


# ---------------- RENDER HEALTH SERVER ----------------

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"2TK Bot is running")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health server running on port {port}")
    server.serve_forever()


# ---------------- DATABASE ----------------

def db_connect():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = db_connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0,
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT,
            status TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def register_user(user):
    conn = db_connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user.id,)
    )

    if cur.fetchone() is None:
        cur.execute(
            """
            INSERT INTO users
            (user_id, username, balance, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                user.id,
                user.username or "",
                0,
                datetime.now().isoformat()
            )
        )
    else:
        cur.execute(
            "UPDATE users SET username = ? WHERE user_id = ?",
            (user.username or "", user.id)
        )

    conn.commit()
    conn.close()


def get_balance(user_id):
    conn = db_connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,)
    )

    result = cur.fetchone()
    conn.close()

    return result[0] if result else 0


def get_orders(user_id):
    conn = db_connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, service, status, created_at
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 10
        """,
        (user_id,)
    )

    result = cur.fetchall()
    conn.close()

    return result


# ---------------- MENU ----------------

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📱 Services", callback_data="services"),
            InlineKeyboardButton("💰 Balance", callback_data="balance"),
        ],
        [
            InlineKeyboardButton("📦 My Orders", callback_data="orders"),
            InlineKeyboardButton("➕ Add Balance", callback_data="add_balance"),
        ],
        [
            InlineKeyboardButton("📜 Terms", callback_data="terms"),
            InlineKeyboardButton("🆘 Support", callback_data="support"),
        ],
        [
            InlineKeyboardButton("🔒 Privacy Policy", url=PRIVACY_URL),
        ],
    ])


# ---------------- COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user)

    await update.message.reply_text(
        "💎 *2TK OTP Numbers Bot* 🤖\n\n"
        "Welcome! 👋\n\n"
        "⚡ Fast • Simple • Automated\n"
        "💰 Starting from ৳2\n\n"
        "Choose an option below:",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user)

    await update.message.reply_text(
        "💎 *2TK Main Menu*\n\nSelect an option:",
        parse_mode="Markdown",
        reply_markup=main_keyboard()
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user)

    amount = get_balance(update.effective_user.id)

    await update.message.reply_text(
        f"💰 *Your Balance*\n\nBalance: ৳{amount:.2f}",
        parse_mode="Markdown"
    )


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user)

    user_orders = get_orders(update.effective_user.id)

    if not user_orders:
        await update.message.reply_text(
            "📦 *My Orders*\n\nYou don't have any orders yet.",
            parse_mode="Markdown"
        )
        return

    text = "📦 *My Orders*\n\n"

    for order_id, service, status, created in user_orders:
        text += (
            f"🆔 #{order_id}\n"
            f"📱 {service}\n"
            f"📌 {status}\n\n"
        )

    await update.message.reply_text(text, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❓ *Help Center*\n\n"
        "/start — Start bot\n"
        "/menu — Main menu\n"
        "/balance — Check balance\n"
        "/orders — View orders\n"
        "/help — Help\n"
        "/privacy — Privacy Policy\n"
        "/terms — Terms\n\n"
        "For support, use the Support button.",
        parse_mode="Markdown"
    )


async def privacy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔒 *Privacy Policy*\n\n{PRIVACY_URL}",
        parse_mode="Markdown"
    )


async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 *Terms of Service*\n\n"
        "• Use this bot only for lawful and authorized purposes.\n"
        "• Do not use the service for spam, fraud, impersonation, "
        "unauthorized access, or bypassing platform security.\n"
        "• Demo services may change or be unavailable.\n"
        "• Payments and real services are not enabled in this demo.",
        parse_mode="Markdown"
    )


# ---------------- BUTTONS ----------------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    register_user(user)

    if query.data == "services":
        await query.message.reply_text(
            "📱 *Services*\n\n"
            "🔹 Authorized Verification Demo\n"
            "💰 Price: ৳2\n"
            "📌 Status: Demo only\n\n"
            "Real provider integration is not enabled.",
            parse_mode="Markdown"
        )

    elif query.data == "balance":
        amount = get_balance(user.id)

        await query.message.reply_text(
            f"💰 *Balance*\n\nYour balance: ৳{amount:.2f}",
            parse_mode="Markdown"
        )

    elif query.data == "orders":
        user_orders = get_orders(user.id)

        if not user_orders:
            await query.message.reply_text(
                "📦 *My Orders*\n\nNo orders found.",
                parse_mode="Markdown"
            )
            return

        text = "📦 *My Orders*\n\n"

        for order_id, service, status, created in user_orders:
            text += (
                f"🆔 #{order_id}\n"
                f"📱 {service}\n"
                f"📌 {status}\n\n"
            )

        await query.message.reply_text(text, parse_mode="Markdown")

    elif query.data == "add_balance":
        await query.message.reply_text(
            "➕ *Add Balance*\n\n"
            "Payment system is currently in demo mode.",
            parse_mode="Markdown"
        )

    elif query.data == "terms":
        await terms(update, context)

    elif query.data == "support":
        await query.message.reply_text(
            "🆘 *Support*\n\n"
            "Please contact the bot operator through the official support channel.",
            parse_mode="Markdown"
        )


# ---------------- MAIN ----------------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")

    init_db()

    # Start Render health server
    threading.Thread(
        target=start_health_server,
        daemon=True
    ).start()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("orders", orders))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("privacy", privacy))
    application.add_handler(CommandHandler("terms", terms))
    application.add_handler(CallbackQueryHandler(button_handler))

    print("2TK Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
