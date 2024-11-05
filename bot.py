import gtts
from gtts import gTTS
from telebot import types
import telebot
import pytgpt.phind as gpt
import os
import requests

bot = telebot.TeleBot("token")

@bot.message_handler(commands=['img'])
def hnd(msg):
    bot.reply_to(msg, "ارسل ماذا تريد ان ارسمه لك 🖼️")
    bot.register_next_step_handler(msg, reqqq)

def reqqq(msg):
    prmpt = msg.text
    url = f"https://image.pollinations.ai/prompt/{prmpt}"
    rsp = requests.get(url)
    
    if rsp.status_code == 200:
        bot.send_photo(msg.chat.id, rsp.url, caption="تم اكتمال الصورة 🖼️")
    else:
        bot.reply_to(msg, "فشل...")

@bot.message_handler(commands=['start'])
def s_w(msg):
    mk = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton(text='قناة المطور', url='https://t.me/telebotcode')
    b2 = types.InlineKeyboardButton(text='مطور البوت', url='https://t.me/DRR_R2')
    b3 = types.InlineKeyboardButton(text='أسالني شمنتضر؟؟؟', url='https://t.me/DRR_R2')

    mk.add(b1, b2, b3)

    txt = '''🌟 مرحبا بك في بوت ذكاء الاصطناعي 🌟
💡 سوف استطيع مساعدتك في أي شي مثل:
🔹 كتابة كودات
🔹 حل مسائل رياضية
🔹 تقديم معلومات جغرافية
🔹 رسم صور باستخدام الأمر /img

📝 ملاحظة: بوت لا يتذكر رسالة سابقة! 
'''

    bot.send_message(msg.chat.id, txt, reply_markup=mk)

@bot.message_handler(func=lambda msg: True)
def e(msg):
    tb = gpt.PHIND()
    w_msg = bot.reply_to(msg, "⏳")
    bot.send_chat_action(msg.chat.id, "find_location")
    txt = tb.chat(msg.text)
    mk = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text='Text to voice', callback_data='cvt')
    mk.add(b1)
    bot.edit_message_text(chat_id=w_msg.chat.id, message_id=w_msg.message_id, text=txt, parse_mode='Markdown', reply_markup=mk)

@bot.callback_query_handler(func=lambda call: call.data == 'cvt')
def cvt_cb(call):
    bot.send_chat_action(call.message.chat.id, "record_audio")
    msg = call.message
    txt = msg.text

    tts = gTTS(txt, lang='ar')
    aud_file = 'audio.mp3'
    tts.save(aud_file)

    bot.send_voice(msg.chat.id, voice=open(aud_file, 'rb'))
    bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=None)
    os.remove(aud_file)

bot.infinity_polling()
