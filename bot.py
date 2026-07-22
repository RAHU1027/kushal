import telebot
from telebot import types
import os
import threading
from flask import Flask

# --- CONFIG ---
API_TOKEN = '5b108bd2fdd31c0c34bc65f24a5216a0'
bot = telebot.TeleBot("8943344174:AAEnYcGFZCKyyZn0wcA_xuLw7mPCA4inRNw")
ADMIN_ID = 8086760320  # <--- Yahan apni Telegram ID dalen
PATH = "./" 
file_id_cache = {} 
USER_FILE = "users.txt"

# --- SIDE MENU ---
def set_menu():
    commands = [
        types.BotCommand("start", "Bot Start Karein"),
        types.BotCommand("users", "Total Users (Admin Only)")
    ]
    bot.set_my_commands(commands)

# --- WEB SERVICE FOR 24/7 ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is running!"
@app.route('/ping')
def ping(): return "Bot is active", 200

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- EXACT VIDEO DATA ---
T1 = """😍 <b>80000+ zip file's Channel</b> 💔
━━━━━━━━━━━━━━━━━━━━
<b>Benefits:</b>
• 📁 All Dark Zip Files Available
• 🆕 New Files Added Daily
• 🔄 Forwarding Files is Allowed

🤔 Want to Buy?
🚀 Offers Are Live Now!

Price: <strike>Rs. 3,999.00</strike> <b>Rs. 999.00</b>
🔥 174 people bought this"""

T2 = """📽️ <b>AVAILABLE VIDEOS COLLECTION</b> 🎁
━━━━━━━━━━━━━━━━━━━━
REAL PRICE - <strike>2499/-</strike>
OFFER PRICE - <b>499/-</b> ✅

VALIDITY ~ 6 MONTH ⌛
PREMIUM QUALITY STUFF ✨

• INCEST ( D@RK )
• SLEEPING PILLS
• ONLY INDIAN

🔥 77 people bought this"""

T3 = """🥷 <b>VIP STUFF AVAILABLE</b> 🇨🇦
━━━━━━━━━━━━━━━━━━━━
Price: <strike>Rs. 299.00</strike> <b>Rs. 149.00</b>
🔥 94 people bought this"""

T4 = """🎀 <b>PREMIUM CUTIES LEAK</b> 🎀
━━━━━━━━━━━━━━━━━━━━
🤡 HELLO USER
Direct P#rn Video Channel 🫧
D#si Maal Ke Deewan 🥀 Ke Liye ✨
51000+ rare D#si le#ks ever.... 😍

Just pay and get entry... 💸
D#rect video - No Ads Sh#t 🚫
Validity :- lifetime ✅

Price: <strike>Rs. 249.00</strike> <b>Rs. 99.00</b>
🔥 55 people bought this"""

T5 = """🔞 <b>PREMIUM DESI MAAL</b> 🍑
━━━━━━━━━━━━━━━━━━━━
Price: <strike>Rs. 259.00</strike> <b>Rs. 69.00</b>
🔥 314 people bought this"""

T6 = """🎬 <b>PREMIUM ADULT COLLECTION UPDATED</b> ✅
━━━━━━━━━━━━━━━━━━━━
MAA-BETA 🖤
BAAP-BETI 🖤
BHAI-BEHEN 🖤
DESI CHOTI BACHIYA 💔
AUNTY AND BHABHI 💔
INSTAGRAM REELS STARS 💔
ONLYFANS FOREIGN 💔
HARDCORE AND FOREPLAY 💔

AND ALL CATEGORIES IN ONE PACKAGE ✊

VALIDITY - 6 MONTH 🤝

🔥🔥 100% MONEY BACK GUARANTEE IF NOT SATISFIED

Price: <strike>Rs. 799.00</strike> <b>Rs. 49.00</b>
🔥 258 people bought this"""

def get_keyboard(p):
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(
        types.InlineKeyboardButton("📽️ WATCH DEMO VIDEO", url="https://t.me/+JBVaDAvX-To1NzRl", style="primary"),
        types.InlineKeyboardButton(f"🔐 PAY Rs. {p} - UNLOCK NOW", callback_data=f"pay_{p}", style="danger"),
        types.InlineKeyboardButton("💬 CONTACT ADMIN", url="t.me/JOD_HEREE_51", style="success")
    )
    return m

def send_fix(uid, f, p, cap):
    full_path = os.path.join(PATH, f)
    markup = get_keyboard(p)
    try:
        if os.path.exists(full_path):
            with open(full_path, 'rb') as file:
                if f.endswith(".mp4"):
                    bot.send_video(uid, file, caption=cap, parse_mode='HTML', reply_markup=markup, supports_streaming=True)
                else:
                    bot.send_photo(uid, file, caption=cap, parse_mode='HTML', reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")

@bot.message_handler(commands=['users'])
def get_users(m):
    if m.chat.id == ADMIN_ID:
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                bot.reply_to(m, f"📊 Total Users Joined: {len(f.readlines())}")
    else:
        bot.reply_to(m, "Sirf Admin access kar sakte hain.")

@bot.message_handler(commands=['start'])
def start(m):
    def save_and_send():
        if not os.path.exists(USER_FILE): 
            open(USER_FILE, "w").close()
        
        user_id_str = str(m.chat.id)
        with open(USER_FILE, "r+") as f:
            content = f.read()
            if user_id_str not in content:
                f.write(f"{user_id_str}\n")
        
        uid = m.chat.id
        data = [
            ("1.jpg", "1,499", T1), ("1.mp4", "499", T2),
            ("2.jpg", "149", T3), ("2.mp4", "99", T4),
            ("3.jpg", "69", T5), ("3.mp4", "49", T6)
        ]
        
        threads = []
        for f, p, cap in data:
            t = threading.Thread(target=send_fix, args=(uid, f, p, cap))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()

    threading.Thread(target=save_and_send).start()

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def callback(call):
    p = call.data.split("_")[1]
    qr_path = "qr.jpg"
    msg_text = f"🔐 <b>Payment — Rs. {p}</b>\n\n📲 QR Code scan karo aur screenshot bhejo!"
    if os.path.exists(qr_path):
        with open(qr_path, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=msg_text, parse_mode='HTML')
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    if m.chat.id != ADMIN_ID:
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ Click To Approve", callback_data=f"ok_{m.chat.id}", style="success"))
        bot.send_message(ADMIN_ID, "User ne payment bheja hai:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ok_"))
def approve(call):
    user_id = call.data.split("_")[1]
    msg = "✅ Payment Verified! Access Mil Gaya!\n\n💋 WATCH VIRAL MEMES FULL VIDEO 💋\n\n⚡️ JOIN OUR CHANNEL\n\n💋 𝐃𝐄𝐒𝐈 𝐌𝐀𝐀𝐋 💋\nhttps://t.me/+DVwN8sdnvDQ1YWE9\n\n❤️‍🔥 𝗝𝗔𝗣𝗔𝗡𝗘𝗦𝗘 𝗛𝗨𝗕 ❤️‍🔥\nhttps://t.me/+b9VNf96P_Z9mNjk1"
    bot.send_message(user_id, msg, parse_mode='HTML')
    bot.edit_message_text("✅ Approved!", call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id)

# --- STARTING ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server).start()
    set_menu()
    print("🚀 BOT LIVE!")
    bot.infinity_polling()
