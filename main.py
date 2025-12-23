# main.py
import os
import time
from telebot import TeleBot, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

bot = TeleBot(BOT_TOKEN)

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("swap", "bypass")
    kb.add("settings")
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id != OWNER_ID:
        return
    bot.send_message(
        message.chat.id,
        "✅ Control Panel Ready",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    if message.chat.id != OWNER_ID:
        return

    if message.text == "swap":
        bot.send_message(message.chat.id, "🟡 Swap job created")

    elif message.text == "bypass":
        bot.send_message(message.chat.id, "🟡 Bypass job created")

    elif message.text == "settings":
        bot.send_message(message.chat.id, "⚙️ Settings panel")

bot.infinity_polling()