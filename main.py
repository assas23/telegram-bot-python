import os
import telebot
from telebot import types

# =====================
# ENV VARIABLES (Railway)
# =====================
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# =====================
# START
# =====================
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id != OWNER_ID:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton("Swap"),
        types.KeyboardButton("Settings"),
        types.KeyboardButton("Status"),
    )

    bot.send_message(
        message.chat.id,
        "✅ <b>Bot Online</b>\nRailway Version",
        reply_markup=kb
    )

# =====================
# MAIN HANDLER
# =====================
@bot.message_handler(func=lambda m: True)
def handler(message):
    if message.chat.id != OWNER_ID:
        return

    if message.text == "Status":
        bot.send_message(message.chat.id, "🟢 Bot running stable on Railway")

    elif message.text == "Settings":
        bot.send_message(message.chat.id, "⚙️ Settings panel")

    elif message.text == "Swap":
        bot.send_message(
            message.chat.id,
            "⚡ Swap command received\n(Logic hooked safely)"
        )

# =====================
# RUN
# =====================
print("Bot started")
bot.infinity_polling()