import requests
import telebot, time, threading
from telebot import types
from gatet import Tele
import os
from func_timeout import func_timeout, FunctionTimedOut

token = '8406430794:AAE2yHzMNiolhVjFclHkBgnL6Bnvv0bgTAA'
bot = telebot.TeleBot(token, parse_mode="HTML")

# ==========================================
# 👇 ALLOWED USERS LIST
ALLOWED_IDS = [
    '1915369904',    # Owner
    '6506125689',     # User 2
    '7745508838',     # User 3
    '6815134572'      # User 4
]
# ==========================================

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) not in ALLOWED_IDS:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return
    bot.reply_to(message, "𝐒𝐞𝐧𝐝 𝐭𝐡𝐞 𝐟𝐢𝐥𝐞 𝐧𝐨𝐰❤️")

# 🔥 NEW FEATURE: Download Lives File 🔥
@bot.message_handler(commands=["getlives"])
def get_lives(message):
    if str(message.chat.id) not in ALLOWED_IDS: return
    
    try:
        if os.path.exists("lives.txt"):
            with open("lives.txt", "rb") as f:
                bot.send_document(message.chat.id, f, caption="✅ <b>Here are your Charged/Live Cards</b>", parse_mode="HTML")
        else:
            bot.reply_to(message, "No Live cards saved yet! ❌")
    except Exception as e:
        bot.reply_to(message, f"Error sending file: {e}")

# 🔥 NEW FEATURE: Clear Lives File 🔥
@bot.message_handler(commands=["clearlives"])
def clear_lives(message):
    if str(message.chat.id) not in ALLOWED_IDS: return
    
    if os.path.exists("lives.txt"):
        os.remove("lives.txt")
        bot.reply_to(message, "🗑️ <b>lives.txt has been cleared!</b>", parse_mode="HTML")
    else:
        bot.reply_to(message, "File is already empty.")

# ==========================================
# 📂 FILE CHECKER LOGIC STARTS HERE
# ==========================================
@bot.message_handler(content_types=["document"])
def main(message):
    if str(message.chat.id) not in ALLOWED_IDS:
        bot.reply_to(message, "You cannot use the bot to contact developers to purchase a bot subscription @Rusisvirus")
        return

    # Threading စတင်ခြင်း
    t = threading.Thread(target=run_checker, args=(message,))
    t.start()

def run_checker(message):
    dd = 0
    live = 0
    ch = 0
    ccn = 0
    cvv = 0
    lowfund = 0
    
    chat_id = message.chat.id
    
    # NAME CONFLICT FIX
    file_name = f"combo_{chat_id}_{int(time.time())}.txt"
    stop_file = f"stop_{chat_id}.stop"

    try:
        ko = bot.reply_to(message, "𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐍𝐨𝐰! 🚀").message_id
        ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
        
        with open(file_name, "wb") as w:
            w.write(ee)
            
        with open(file_name, 'r') as file:
            lino = file.readlines()
            total = len(lino)
            
            for cc in lino:
                cc = cc.strip()
                
                # ===== STOP CHECK =====
                if os.path.exists(stop_file):
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text='𝑺𝑻𝑶𝑷 ✅\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus')
                    os.remove(stop_file)
                    if os.path.exists(file_name): os.remove(file_name)
                    return
                
                # ===== BIN LOOKUP =====
                try:
                    data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
                except:
                    data = {}
                
                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '')
                bank = data.get('bank', 'Unknown')
                
                start_time = time.time()
                
                # ===== CHECKER WITH TIMEOUT =====
                try:
                    # 25 seconds timeout
                    last = str(func_timeout(25, Tele, args=(cc,)))
                except FunctionTimedOut:
                    last = 'Gateway Time Out ❌'
                except Exception as e:
                    print(e)
                    last = 'Error'
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # 🔥 FIX: STATUS CLEANING (JSON ရှင်းထုတ်ခြင်း) 🔥
                # ဒီနေရာမှာ Status ကို အရင်သန့်လိုက်မှ Dashboard မှာ အရှည်ကြီးမပေါ်မှာ
                if "Payment Successful" in last:
                    display_status = "Charged ✅"
                elif "funds" in last:
                    display_status = "Insufficient Funds 🍃"
                elif "security code" in last:
                    display_status = "CCN Live ✅"
                elif "success" in last and "false" in last: # JSON Error Catch
                    display_status = "Declined ❌"
                elif "Stripe Error" in last or "declined" in last:
                    display_status = "Declined ❌"
                else:
                    display_status = "Declined ❌"

                # ===== DASHBOARD VIEW =====
                view_text = f"""\
• <code>{cc}</code>

🟢 sᴛᴀᴛᴜs  ➜ <code>{display_status}</code>

💳 ᴄʜᴀʀɢᴇᴅ  ➜ <code>[ {ch} ]</code>

🔐 ᴄᴄɴ ➜ <code>[ {ccn} ]</code>

🔐 ᴄᴠᴠ ➜ <code>[ {cvv} ]</code>

⚠️ ʟᴏᴡ ғᴜɴᴅs ➜ <code>[ {lowfund} ]</code>

📊 ᴅᴇᴄʟɪɴᴇᴅ ➜ <code>[ {dd} ]</code>

• ᴛᴏᴛᴀʟ ➜ <code>[ {total} ]</code>
"""
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton("⛔ sᴛᴏᴘ ⚠️", callback_data="stop"))
                
                # Check Logic
                if 'Payment Successful' in last:
                    ch += 1
                    # Save Charge
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - Charged ✅ - {bank} ({country})\n")
                    
                    msg = f''' 
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕!🥵</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                
                elif 'funds' in last:
                    lowfund += 1
                    # Save Low Funds
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - Low Funds 🍃\n")
                    
                    msg = f'''			
𝐂𝐀𝐑𝐃: <code>{cc}</code>
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: <code>𝙸𝚗𝚜𝚞𝚏𝚏𝚒𝚌𝚒𝚎𝚗𝚝 𝚏𝚞𝚗𝚍𝚜 😂</code>

𝐁𝐢𝐧 𝐈𝐧𝐟𝐨: <code>{cc[:6]}-{card_type} - {brand}</code>
𝐁𝐚𝐧𝐤: <code>{bank}</code>
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: <code>{country} - {country_flag}</code>

𝐓𝐢𝐦𝐞: <code>1{"{:.1f}".format(execution_time)} second</code> 
𝐁𝐨𝐭 𝐀𝐛𝐨𝐮𝐭: @Rusisvirus'''
                    bot.reply_to(message, msg)
                
                elif 'security code' in last:
                    ccn += 1
                elif 'action' in last or '3D' in last:
                    # 3DS Logic
                    cvv += 1
                    with open("lives.txt", "a") as f:
                        f.write(f"{cc} - 3DS ⚠️\n")
                else:
                    dd += 1
                
                # Update Dashboard every 15 cards or if hit found
                if (ch + lowfund + ccn + cvv + dd) % 15 == 0 or 'Payment Successful' in last or 'funds' in last:
                    bot.edit_message_text(chat_id=chat_id, message_id=ko, text=view_text, reply_markup=markup)
                
                # Console Log
                print(f"{chat_id} : {cc} -> {display_status}")

        # Cleanup input file only
        if os.path.exists(file_name): os.remove(file_name)
        bot.edit_message_text(chat_id=chat_id, message_id=ko, text='𝑪𝒉𝒆𝒄𝒌𝒊𝒏𝒈 𝑫𝒐𝒏𝒆!\n𝑩𝒐𝒕 𝑩𝒚 ➜ @Rusisvirus')

    except Exception as e:
        print(f"Error for {chat_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
    stop_file = f"stop_{call.message.chat.id}.stop"
    with open(stop_file, "w") as file:
        pass
    bot.answer_callback_query(call.id, "Stopping...")

# ===== SAFE POLLING =====
import telebot.apihelper as apihelper
apihelper.REQUEST_TIMEOUT = 30

while True:
    try:
        bot.polling(non_stop=True, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print("Polling error:", e)
        time.sleep(5)
