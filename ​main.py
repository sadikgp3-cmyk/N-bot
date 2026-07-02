import os
import requests
import asyncio
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# আপনার তথ্যসমূহ
API_KEY = "ZNX_LRH8MNQ67WUJ6SBR8SX4X0CP"
BOT_TOKEN = "8994785225:AAG3JDNLs3qH1bc4QMCz08qYI_xwg9mILg0"
ADMIN_ID = "8514892358"

bot = Bot(token=BOT_TOKEN)

# Zenex থেকে নম্বর নেওয়ার ফাংশন
def get_number_from_zenex(service):
    url = "https://api.zenexnetwork.com/v1/getnum"
    headers = {'mapikey': API_KEY}
    payload = {"range": "4473845XXX", "is_national": False, "remove_plus": False}
    try:
        response = requests.post(url, json=payload, headers=headers).json()
        return response['data']['number']
    except:
        return None

# মেনু তৈরি করা
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("WhatsApp", callback_data='WA'), InlineKeyboardButton("Telegram", callback_data='TG')],
        [InlineKeyboardButton("Instagram", callback_data='IG'), InlineKeyboardButton("Facebook", callback_data='FB')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("প্ল্যাটফর্ম সিলেক্ট করুন:", reply_markup=reply_markup)

# বাটন ক্লিক হ্যান্ডলার
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    service = query.data
    number = get_number_from_zenex(service)
    await query.edit_message_text(f"আপনার {service} নম্বর: `{number}` \n\nঅপেক্ষা করুন, OTP এলে জানানো হবে।", parse_mode='Markdown')

# SMS/OTP চেক করা (ব্যাকগ্রাউন্ডে চলবে)
async def sms_monitor():
    while True:
        try:
            response = requests.get("https://api.zenexnetwork.com/v1/numsuccess/info", headers={'mapikey': API_KEY}).json()
            otps = response['data']['otps']
            for msg in otps:
                await bot.send_message(chat_id=ADMIN_ID, text=f"📩 **নতুন OTP:**\n{msg['otp']}", parse_mode='Markdown')
        except:
            pass
        await asyncio.sleep(5)

# বট রান করা
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    # ব্যাকগ্রাউন্ড টাস্ক চালু করা
    loop = asyncio.get_event_loop()
    loop.create_task(sms_monitor())
    
    print("বট সচল হয়েছে...")
    app.run_polling()
