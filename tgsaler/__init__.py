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

class group:

    def __init__(self, group_data):
        global all_positions
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.markup.add(types.KeyboardButton("Назад"))
        self.markup.add(types.KeyboardButton("Корзина"))
        self.positions = []
        for el in group_data:
            print(el)
            new_name = (
                el[props["Name"]]
                + ", "
                + str(el[props["Price"]])
                + " "
                + props["currency"]
            )
            self.positions.append(new_name)
            all_descr[new_name] = el[props["Descr"]]
            all_prices[new_name] = el[props["Price"]]
            all_images[new_name] = el[props["foto"]]

        for el in self.positions:
            self.markup.add(types.KeyboardButton(el))
        all_positions = all_positions + self.positions

    def check(self, x):
        return x in self.positions

    def markup(self):
        return self.markup


tmp_menu_categories = list(os.listdir(props["menufolder"]))
group_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
group_markup.add(types.KeyboardButton("Корзина"))

groupdone_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
groupdone_markup.add(types.KeyboardButton("Всё верно"))
groupdone_markup.add(types.KeyboardButton("Продолжить покупки"))
groupdone_markup.add(types.KeyboardButton("Убрать товар"))

deliver_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
deliver_markup.add(types.KeyboardButton("С собой"))
deliver_markup.add(types.KeyboardButton("Доставка"))

bin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bin_markup.add(types.KeyboardButton("Да"))
bin_markup.add(types.KeyboardButton("Нет"))

menu_categories = [
    t[:-4] for t in tmp_menu_categories if len(t) > 3 and t[-3:] == "csv"
]
group_list = {}
for gr in menu_categories:
    opend_group = pd.read_csv(props["menufolder"] + "/" + gr + ".csv").to_dict(
        "records"
    )
    group_list[gr] = group(opend_group)
for cat in menu_categories:
    group_markup.add(types.KeyboardButton(cat))
del tmp_menu_categories
