# -*- coding: utf-8 -*-

import telebot
import random
import config
import logging
import editor

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

nick = ''
fin_nick = ''
replace_values = {"s": "$", "ч": "4", "с": "s", "д": "D"}

@bot.message_handler(commands=["start"])
def welcome(message):
    sti = open('sticker/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Подобрать ник~")
    item2 = types.KeyboardButton("Статус для ВК^^")
    item3 = types.KeyboardButton("*Аватарки для форумов*")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     "Приветик, <b>{0.first_name}</b>! \nЯ бот, посвященный нулевым =)\nЯ могу сгенерировать тебе случайный никнейм, статус или аву~~".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, 'Я могу сгенерировать тебе:\n/random_nickname\n/my_nickname\n/status\n/avatar\nТыкай (^-^)')

@bot.message_handler(commands=["my_nickname"])
def send_nickname(message):
    bot.send_message(message.chat.id, 'Напиши сюда текст (например, свое имя) и я его настрою^^')
    bot.register_next_step_handler(message, fin_nick)

def gen_nick(message):
    global nick
    nick = message.text
    generated_nick = editor.multiple_replace(nick, replace_values)
    return generated_nick

def fin_nick(message):
    fin_nick = gen_nick(message)
    final_generated_nick = editor.to_weird_case(fin_nick)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/my_nickname")
    item2 = types.KeyboardButton("/help")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, f'{final_generated_nick}', reply_markup=markup)

@bot.message_handler(commands=["random_nickname"])
def random_nickname(message):
    nickname = random.choice(config.nicknames)
    bot.send_message(message.chat.id, nickname)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private':
        if message.text == 'Подобрать ник~' or message.text == '/nickname':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("/random_nickname")
            item2 = types.KeyboardButton("/my_nickname")

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Я могу сгенерировать тебе:\n/random_nickname - случайный\n/my_nickname - на основе твоего\nТыкай (^-^)', reply_markup=markup)
        elif message.text == 'Подобрать ник~' or message.text == '/random_nickname':
            nickname = random.choice(config.nicknames)
            bot.send_message(message.chat.id, nickname)
        elif message.text == '*Аватарки для форумов*' or message.text == '/avatar':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton("Аниме \(^_^)/", callback_data='anime_pic')
            item2 = types.InlineKeyboardButton("Эмо..(", callback_data='emo_pic')
            item3 = types.InlineKeyboardButton("Dля Dево4еk***", callback_data='girly_pic')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, "*~Выбери тип аватарки~*", reply_markup=markup)
        elif message.text == 'Статус для ВК^^' or message.text == '/status':
            vk_quote = random.choice(config.vk_quotes)
            bot.send_message(message.chat.id, vk_quote)
        elif message.text == '/help':
            bot.send_message(message.chat.id, 'Я могу сгенерировать тебе:\n/nickname\n/status\n/avatar\n(^-^)')
        else:
            bot.send_message(message.chat.id, "Я тебя не понимаю =( Напиши /help")


@bot.callback_query_handler(func=lambda call: True)
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


bot.infinity_polling(timeout=10, long_polling_timeout=5)