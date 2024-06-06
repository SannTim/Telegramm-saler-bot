import telebot
from telebot import types
import json
import os
import pandas as pd

with open("config.json") as f:
    props = json.load(f)
bot = telebot.TeleBot(props["token"], parse_mode=None)
all_positions = []
all_prices = {}
all_descr = {}
all_images = {}
admin_usres = []
admin_ids = []
all_orders = {}
orders_id = 1


def orders_send():
    orders_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    msg = "\n".join(all_orders)
    if len(all_orders) == 0:
        return
    for el in all_orders:
        # print(el)
        # print(el[0])
        orders_markup.add(types.KeyboardButton(str(el[0])))
    for admin in admin_usres:
        bot.send_message(admin, msg)
        bot.send_message(admin, "Какой заказ готов?")


def form_bin_mes(usr):
    ans = "В вашей корзине сейчас:\n"
    for el in usr["bin"]:
        if usr["bin"][el] != 1:
            ans += "x" + str(usr["bin"][el]) + ": "
        ans += el + "\n"
    ans += "Сумма:" + str(usr["price"])
    return ans


def form_order(usr, st, id, name):
    # print(id)
    ans = str(id) + " заказ:\n"
    ans += "От пользователя: @" + name + "\n"
    for el in usr["bin"]:
        if usr["bin"][el] != 1:
            ans += "x" + str(usr["bin"][el]) + ": "
        ans += el + "\n"
    ans += "На сумму:" + str(usr["price"]) + "\n" + st
    return ans
