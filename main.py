import os
import time
import 
BOT_TOKEN = 8142747304:AAHXFIgCyyBc5mai3caH7j5HTfUgKkRXRCI
OWNER_ID = 1087753450

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing")
if not OWNER_ID:
    raise RuntimeError("OWNER_ID is missing")

OWNER_ID = int(OWNER_ID)

# ====== BOT ======
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ====== JOB QUEUE ======
job_queue = queue.Queue()
job_status = {}  # job_id -> status text

def job_worker():
    """Background worker that executes jobs safely (Railway-friendly)."""
    while True:
        job_id, job_type, payload = job_queue.get()
        try:
            job_status[job_id] = "🟡 Running"
            # ---- PLACE YOUR HEAVY LOGIC HERE (STEP-BY-STEP) ----
            # IMPORTANT: keep it incremental with sleeps to avoid crashes
            steps = payload.get("steps", 10)
            for i in range(steps):
                time.sleep(0.5)  # pacing prevents Railway crash
                job_status[job_id] = f"🟡 Running ({i+1}/{steps})"
            # ---------------------------------------------------
            job_status[job_id] = "🟢 Done"
        except Exception as e:
            job_status[job_id] = f"🔴 Error: {e}"
        finally:
            job_queue.task_done()

# Start worker thread
threading.Thread(target=job_worker, daemon=True).start()

# ====== UI ======
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("swap", "bypass")
    kb.add("status", "settings")
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.id != OWNER_ID:
        return
    bot.send_message(
        message.chat.id,
        "✅ Bot is running on Railway\nاختر أمر:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    if message.chat.id != OWNER_ID:
        return

    text = message.text.lower().strip()

    if text == "swap":
        job_id = f"job_{int(time.time())}"
        job_status[job_id] = "🟠 Queued"
        job_queue.put((job_id, "swap", {"steps": 20}))
        bot.send_message(message.chat.id, f"🟡 Swap job created\nID: {job_id}")

    elif text == "bypass":
        job_id = f"job_{int(time.time())}"
        job_status[job_id] = "🟠 Queued"
        job_queue.put((job_id, "bypass", {"steps": 15}))
        bot.send_message(message.chat.id, f"🟡 Bypass job created\nID: {job_id}")

    elif text == "status":
        if not job_status:
            bot.send_message(message.chat.id, "ℹ️ No jobs yet")
        else:
            msg = "\n".join([f"{k}: {v}" for k, v in list(job_status.items())[-5:]])
            bot.send_message(message.chat.id, f"<b>Jobs:</b>\n{msg}")

    elif text == "settings":
        bot.send_message(message.chat.id, "⚙️ Settings panel (ready)")

    else:
        bot.send_message(message.chat.id, "❓ أمر غير معروف")

# ====== SAFE POLLING LOOP ======
while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)