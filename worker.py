import telebot
import threading
import sqlite3

# Token file se read karega
with open("token.txt", "r") as f:
    MANAGER_TOKEN = f.read().strip()

bot = telebot.TeleBot(MANAGER_TOKEN)

# Baaki sab logic...
conn = sqlite3.connect('user_bots.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS bots (user_id INTEGER PRIMARY KEY, token TEXT)')
conn.commit()

# --- Baki ka logic... (Start_user_bot aur baki commands same rahengi) ---
def start_user_bot(token):
    try:
        u_bot = telebot.TeleBot(token)
        u_bot.infinity_polling()
    except Exception as e:
        print(f"Bot Error: {e}")

@bot.message_handler(commands=['connect'])
def connect(message):
    msg = bot.reply_to(message, "Bot connect karne ke liye token bhejo:")
    bot.register_next_step_handler(msg, save_and_run)

def save_and_run(message):
    token = message.text.strip()
    user_id = message.chat.id
    cursor.execute('INSERT OR REPLACE INTO bots VALUES (?, ?)', (user_id, token))
    conn.commit()
    threading.Thread(target=start_user_bot, args=(token,), daemon=True).start()
    bot.reply_to(message, "✅ Bot successfully connected and running!")

if __name__ == "__main__":
    bot.infinity_polling()
