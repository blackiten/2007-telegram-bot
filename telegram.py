# -*- coding: utf-8 -*-

import telebot
import random
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    sti = open('sticker/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Подобрать ник~")
    item2 = types.KeyboardButton("Статус для ВК^^")
    item3 = types.KeyboardButton("*Аватарки для форумов*")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Приветик, <b>{0.first_name}</b>! \nЯ бот, посвященный нулевым =)\nЯ могу сгенерировать тебе случайный никнейм, статус или аву~~".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private':
        if message.text == 'Подобрать ник~':
            nickname = random.choice(config.nicknames)
            bot.send_message(message.chat.id, nickname)
        elif message.text == '*Аватарки для форумов*':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Аниме \(^_^)/", callback_data='anime_pic')
            item2 = types.InlineKeyboardButton("Эмо..(", callback_data='emo_pic')
            item3 = types.InlineKeyboardButton("Dля Dево4еk***", callback_data='girly_pic')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, "*~Выбери тип аватарки~*", reply_markup=markup)
        # elif message.text == 'Цитаты для тебя<3':
        #
        #     markup = types.InlineKeyboardMarkup(row_width=1)
        #     item1 = types.InlineKeyboardButton("Веселое))", callback_data='good')
        #     item2 = types.InlineKeyboardButton("Грустное((((", callback_data='bad')
        #     item3 = types.InlineKeyboardButton("Дерзкое;)))", callback_data='cheeky')
        #     item4 = types.InlineKeyboardButton("Задумчивое....", callback_data='wise')
        #
        #     markup.add(item1, item2, item3, item4)
        #
        #     bot.send_message(message.chat.id, "Какое у тебя настроение??", reply_markup=markup)
        elif message.text == 'Статус для ВК^^':
            vk_quote = random.choice(config.vk_quotes)
            bot.send_message(message.chat.id, vk_quote)
        elif message.text == '/help':
            bot.send_message(message.chat.id, 'Я могу сгенерировать тебе случайный ник, статус или аву, для этого нажми на кнопки внизу (^-^)')
        else:
            bot.send_message(message.chat.id, "Я тебя не понимаю =( Напиши /help")

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
     try:
         if call.message:
             if call.data == 'anime_pic':
                 anime_pic = open(random.choice(config.anime_pics), 'rb')
                 bot.send_animation(call.message.chat.id, anime_pic)
             elif call.data == 'emo_pic':
                 emo_pic = open(random.choice(config.emo_pics), 'rb')
                 bot.send_animation(call.message.chat.id, emo_pic)
             elif call.data == 'girly_pic':
                 girly_pic = open(random.choice(config.girly_pics), 'rb')
                 bot.send_animation(call.message.chat.id, girly_pic)

     except Exception as e:
         print(repr(e))

# @bot.callback_query_handler(func=lambda call:True)
# def callback_inline(call):
#     try:
#         if call.message:
#             if call.data == 'good':
#                 bot.send_message(call.message.chat.id, "Здесь будет веселый статус")
#             elif call.data == 'bad':
#                 bot.send_message(call.message.chat.id, "Здесь будет грустный статус")
#             elif call.data == 'cheeky':
#                 cheeky_quote = random.choice(config.cheeky_quotes)
#                 bot.send_message(message.chat.id, cheeky_quote)
#             elif call.data == 'wise':
#                 wise_quote = random.choice(config.wise_quotes)
#                 bot.send_message(call.message.chat.id, wise_quote)
#
#     except Exception as e:
#         print(repr(e))
# RUN

bot.polling(none_stop=True, interval=0)