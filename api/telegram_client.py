#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import json,requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

curr_state = [[0,0,0],[0,0,0],[0,0,0]]

user_room = dict()
user_uid = dict()
find_room_map = dict()
opossiters = dict()



def start(bot, update):
    update.message.reply_text("hey you can start new game by /init or join current game by /join TOKEN_ROOM ")



def button(bot, update):
    keyboard = [[InlineKeyboardButton("{}".format(curr_state[0][0]), callback_data='00'),
                 InlineKeyboardButton("{}".format(curr_state[0][1]), callback_data='01'),
                 InlineKeyboardButton("{}".format(curr_state[0][2]), callback_data='02')],

                [InlineKeyboardButton("{}".format(curr_state[1][0]), callback_data='10'),
                 InlineKeyboardButton("{}".format(curr_state[1][1]), callback_data='11'),
                 InlineKeyboardButton("{}".format(curr_state[1][2]), callback_data='12')],

                [InlineKeyboardButton("{}".format(curr_state[2][0]), callback_data='20'),
                 InlineKeyboardButton("{}".format(curr_state[2][1]), callback_data='21'),
                 InlineKeyboardButton("{}".format(curr_state[2][2]), callback_data='22')]
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    #update.message.reply_text('Please choose:', reply_markup=reply_markup)

    query = update.callback_query
    print(query.data[0], query.data[1])
    curr_state[int(query.data[0])][int(query.data[1])] = 1
    print(query.message.chat_id)
    send_msg(bot, update, reply_markup)
    bot.edit_message_text(text="game_grid",reply_markup=reply_markup,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)



def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def set_user_to_game(tguid, token):
    user_room[tguid] = token

def find_room(tguid, token):
    user_room[token] = tguid

def set_user_to_uid(tgid,uid):
    user_uid[tgid] = uid


def init_game(bot, update):
    game_token = json.loads(requests.get("http://0.0.0.0:5000/init").text)
    tguid = update.message.chat_id
    set_user_to_game(tguid,game_token)
    find_room(tguid,game_token)
    get_user = json.loads(requests.get("http://0.0.0.0:5000/curraddress").text)["accounts_list"]
    set_user_to_uid(tguid, get_user[0])
    update.message.reply_text("your game token: {} ".format(game_token))



def join(bot, update):
    keyboard = [[InlineKeyboardButton("{}".format(curr_state[0][0]), callback_data='00'),
                 InlineKeyboardButton("{}".format(curr_state[0][1]), callback_data='01'),
                 InlineKeyboardButton("{}".format(curr_state[0][2]), callback_data='02')],

                [InlineKeyboardButton("{}".format(curr_state[1][0]), callback_data='10'),
                 InlineKeyboardButton("{}".format(curr_state[1][1]), callback_data='11'),
                 InlineKeyboardButton("{}".format(curr_state[1][2]), callback_data='12')],

                [InlineKeyboardButton("{}".format(curr_state[2][0]), callback_data='20'),
                 InlineKeyboardButton("{}".format(curr_state[2][1]), callback_data='21'),
                 InlineKeyboardButton("{}".format(curr_state[2][2]), callback_data='22')]
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    token = update.message.text.split()[1]
    if token not in user_room:
        print("nihuya")
    opponent = user_room[token]
    tguid = update.message.chat_id
    set_user_to_game(tguid,token)
    get_user = json.loads(requests.get("http://0.0.0.0:5000/curraddress").text)["accounts_list"]
    set_user_to_uid(tguid, get_user[1])
    opossiters[tguid] = opponent
    opossiters[opponent] = tguid
    send_init_message(bot, update)
    update.message.reply_text("game grid ", reply_markup=reply_markup)




def send_init_message(bot,update):
    keyboard = [[InlineKeyboardButton("{}".format(curr_state[0][0]), callback_data='00'),
                 InlineKeyboardButton("{}".format(curr_state[0][1]), callback_data='01'),
                 InlineKeyboardButton("{}".format(curr_state[0][2]), callback_data='02')],

                [InlineKeyboardButton("{}".format(curr_state[1][0]), callback_data='10'),
                 InlineKeyboardButton("{}".format(curr_state[1][1]), callback_data='11'),
                 InlineKeyboardButton("{}".format(curr_state[1][2]), callback_data='12')],

                [InlineKeyboardButton("{}".format(curr_state[2][0]), callback_data='20'),
                 InlineKeyboardButton("{}".format(curr_state[2][1]), callback_data='21'),
                 InlineKeyboardButton("{}".format(curr_state[2][2]), callback_data='22')]
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.sendMessage(text=" game grid ",
                    chat_id=opossiters[update.message.chat_id], reply_markup=reply_markup)


def send_msg(bot, update, reply_markup):

    bot.sendMessage(text=" game grid ",
                          chat_id=opossiters[update.callback_query.message.chat_id], reply_markup=reply_markup)






def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("533117196:AAFAl5AWrIRrN9qniJnVPL--Tz4AorcAdbc")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('init', init_game))
    updater.dispatcher.add_handler(CommandHandler('join', join))


    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()