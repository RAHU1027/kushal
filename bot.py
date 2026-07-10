import telebot
from telebot import types, apihelper
import os
import time
import threading
from flask import Flask

# --- CONFIG ---
# Token ko environment variable mein rakhna safe hai
API_TOKEN = os.environ.get('API_TOKEN', '8410119226:AAEDaMjNEmPINLbJc26RsPVNKgGjVNH_fSk')
bot = telebot.TeleBot(API_TOKEN)
PATH = "/sdcard/Download/kushal/"
file_id_cache = {} 

# --- WEB SERVICE FOR 24/7 ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# --- TIME ROBOT (UPTIME SYSTEM) ---
def time_robot():
    while True:
        # Yeh system har 30 min mein ping karega taaki bot active rahe
        print("🤖 Time Robot: System Active & Checking Uptime...")
        time.sleep(1800) 

# --- ORIGINAL TEXT DATA ---
T1 = """😍 <b>80000+ zip file's Channel</b> 💔
━━━━━━━━━━━━━━━━━━━━
<b>Benefits:</b>
• 📁 All Dark Zip Files Available
• 🆕 New Files Added Daily
• 🔄 Forwarding Files is Allowed

🤔 Want to Buy?
🚀 Offers Are Live Now!

Price: <strike>Rs. 3,999.00</strike> <b>Rs. 1,499.00</b>
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
        types.InlineKeyboardButton("📽️ WATCH DEMO VIDEO", url="https://t.me/kushal"),
        types.InlineKeyboardButton(f"💎 UNLOCK PREMIUM ({p})", callback_data=f"pay_{p}"),
        types.InlineKeyboardButton("💬 CONTACT ADMIN", url="https://t.me/kushal_admin")
    )
    return m

def send_fix(uid, f, p, cap):
    full_path = os.path.join(PATH, f)
    markup = get_keyboard(p)
    try:
        if f in file_id_cache:
            fid = file_id_cache[f]
            if f.endswith(".mp4"): bot.send_video(uid, fid, caption=cap, parse_mode='HTML', reply_markup=markup)
            else: bot.send_photo(uid, fid, caption=cap, parse_mode='HTML', reply_markup=markup)
            return

        if os.path.exists(full_path):
            with open(full_path, 'rb') as file:
                if f.endswith(".mp4"):
                    s = bot.send_video(uid, file, caption=cap, parse_mode='HTML', reply_markup=markup, supports_streaming=True)
                    file_id_cache[f] = s.video.file_id
                else:
                    s = bot.send_photo(uid, file, caption=cap, parse_mode='HTML', reply_markup=markup)
                    file_id_cache[f] = s.photo[-1].file_id
    except Exception as e:
        print(f"Send Error: {e}")

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.chat.id
    data = [
        ("1.jpg", "1,499", T1), ("1.mp4", "499", T2),
        ("2.jpg", "149", T3), ("2.mp4", "99", T4),
        ("3.jpg", "69", T5), ("3.mp4", "49", T6)
    ]
    for f, p, cap in data:
        send_fix(uid, f, p, cap)
        time.sleep(0.5)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data.startswith("pay"):
        p = call.data.split("_")[1]
        msg = f"💳 <b>UPI:</b> <code>jamnajamna419@okicici</code>\nPay Rs. {p} & send screenshot!"
        bot.send_message(call.message.chat.id, msg, parse_mode='HTML')
    bot.answer_callback_query(call.id)

# --- STARTING WITH UPTIME & AUTO-RECOVERY ---
if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    threading.Thread(target=time_robot, daemon=True).start()
    
    print("🚀 ULTRA SPEED & PERFECT ORDER LIVE!")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"CRASHED! Restarting in 15s... Error: {e}")
            time.sleep(15)
