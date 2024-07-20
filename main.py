import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from config import token
from logic import *

bot = telebot.TeleBot(token)

def gen_markup_for_text():
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton('Получить ответ', callback_data='text_ans'),
                   InlineKeyboardButton('Перевести сообщение', callback_data='text_translate'))
        
        return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if "text" in call.data:
        obj = TextAnalysis.memory[call.from_user.username][-1]
        if call.data == "text_ans":
            bot.send_message(call.message.chat.id, obj.response)
        elif call.data == "text_translate":
            bot.send_message(call.message.chat.id,  obj.translation)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    
    TextAnalysis(message.text, message.from_user.username)
    
    
    chat_id = message.chat.id
    text = "Я получил твое сообщение! Что ты хочешь с ним сделать?"
    
    bot.send_chat_action(chat_id, 'typing')  #
    time.sleep(1) 
    
    bot.send_message(chat_id, text, reply_markup=gen_markup_for_text())

bot.infinity_polling(none_stop=True)