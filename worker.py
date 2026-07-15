import telebot
import threading
import sqlite3
from telebot import types

# 1. Token Read
with open("token.txt", "r") as f:
    MANAGER_TOKEN = f.read().strip()

bot = telebot.TeleBot(MANAGER_TOKEN)

# 2. Database Setup
conn = sqlite3.connect('user_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bots 
                  (user_id INTEGER PRIMARY KEY, token TEXT, qr_id TEXT, upi TEXT)''')
conn.commit()

# 3. Side Menu Setup
def set_bot_menu():
    commands = [
        types.BotCommand("connect", "Apna Bot Connect Karein"),
        types.BotCommand("edit_qr", "QR Code Edit Karein"),
        types.BotCommand("edit_upi", "UPI ID Edit Karein"),
        types.BotCommand("list", "Active Bots"),
        types.BotCommand("help", "Help")
    ]
    bot.set_my_commands(commands)

# 4. Logic Functions
def start_user_bot(token):
    try:
        u_bot = telebot.TeleBot(token)
        u_bot.infinity_polling()
    except Exception as e:
        print(f"Bot Error: {e}")

# --- COMMANDS ---
@bot.message_handler(commands=['start', 'help'])
def help_cmd(message):
    bot.reply_to(message, "Welcome! Menu se options chunein.")

@bot.message_handler(commands=['connect'])
def connect(message):
    msg = bot.reply_to(message, "Apne bot ka Token bhejo:")
    bot.register_next_step_handler(msg, save_token)

def save_token(message):
    token = message.text.strip()
    user_id = message.chat.id
    cursor.execute('INSERT OR REPLACE INTO bots (user_id, token) VALUES (?, ?)', (user_id, token))
    conn.commit()
    threading.Thread(target=start_user_bot, args=(token,), daemon=True).start()
    bot.reply_to(message, "✅ Bot Connect ho gaya!")

@bot.message_handler(commands=['edit_qr'])
def edit_qr(message):
    msg = bot.reply_to(message, "Naya QR Code (Photo) bhejo:")
    bot.register_next_step_handler(msg, save_qr)

def save_qr(message):
    if message.content_type == 'photo':
        fid = message.photo[-1].file_id
        cursor.execute('UPDATE bots SET qr_id = ? WHERE user_id = ?', (fid, message.chat.id))
        conn.commit()
        bot.reply_to(message, "✅ QR Code update ho gaya!")
    else:
        bot.reply_to(message, "❌ Sirf photo bhejiye!")

@bot.message_handler(commands=['edit_upi'])
def edit_upi(message):
    msg = bot.reply_to(message, "Nayi UPI ID bhejo:")
    bot.register_next_step_handler(msg, save_upi)

def save_upi(message):
    upi = message.text
    cursor.execute('UPDATE bots SET upi = ? WHERE user_id = ?', (upi, message.chat.id))
    conn.commit()
    bot.reply_to(message, f"✅ UPI update ho gaya: {upi}")

@bot.message_handler(commands=['list'])
def list_bots(message):
    cursor.execute('SELECT user_id FROM bots')
    bots = cursor.fetchall()
    bot.reply_to(message, f"📊 Total Active Bots: {len(bots)}")

# 5. Initialization
if __name__ == "__main__":
    set_bot_menu()
    cursor.execute('SELECT token FROM bots')
    for row in cursor.fetchall():
        threading.Thread(target=start_user_bot, args=(row[0],), daemon=True).start()
    print("🚀 Manager Bot is Live!")
    bot.infinity_polling()
