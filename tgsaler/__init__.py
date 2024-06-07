import telebot
from telebot import types
import json
import os
import pandas as pd
import time
from bd_worker import db_controller
with open("config.json") as f:
    props = json.load(f)

bot = telebot.TeleBot(props["token"], parse_mode=None)
bd = db_controller()
all_positions = []
all_prices = {}
all_descr = {}
all_images = {}
admin_usres = []
admin_ids = []
all_orders = {}
orders_id = 1


group_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
groupdone_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
deliver_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
group_list = {}

def update_markups():
    global group_markup, groupdone_markup, deliver_markup, bin_markup, group_list
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

def updater():
    update_markups()
    time.sleep(10)

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




@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    cid = message.chat.id
    with open(str(props["users_folder"]) + "/" + str(message.from_user.id), "w") as f:
        usr = {}
        usr["prev"] = "start"
        usr["bin"] = {}
        usr["price"] = 0
        json.dump(usr, f)
    sti = open("stikers/AnimatedSticker.tgs", "rb")
    bot.send_sticker(cid, sti)
    for m in props["Welcome messages"]:
        bot.send_message(cid, m)
    bot.send_message(cid, "Выберите категорию меню", reply_markup=group_markup)



@bot.message_handler(content_types="text")
def category_go(message):
    global orders_id
    # print(message.from_user)
    if message.from_user.id in admin_ids:

        # print("tut")

        for el in all_orders:
            print(el[: len(message.text)])
            print(message.text)
            if el[: len(message.text)] == message.text:
                bot.send_message(all_orders[el], "Ваш заказ готов!")
                bot.send_message(
                    all_orders[el], "Выберите категорию меню", reply_markup=group_markup
                )
                del all_orders[el]
                orders_send()
                return

        return

    cid = message.chat.id
    if message.text in menu_categories:
        bot.send_message(
            cid,
            "Выберите продукт из группы",
            reply_markup=group_list[message.text].markup,
        )
    elif message.text == "Назад":
        bot.send_message(cid, "Выберите категорию меню", reply_markup=group_markup)
    elif message.text in all_positions:
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
        if usr["prev"] == "Убрать товар":
            usr["price"] -= usr["bin"][message.text] * all_prices[message.text]
            del usr["bin"][message.text]

            with open(
                props["users_folder"] + "/" + str(message.from_user.id), "w"
            ) as f:
                json.dump(usr, f)
            bot.send_message(cid, "Проверьте, что в корзине все верно")
            bot.send_message(cid, form_bin_mes(usr), reply_markup=groupdone_markup)
            return
        try:
            im = open("images/" + all_images[message.text], "rb")
            bot.send_photo(cid, im)
        except Exception:
            bot.send_message(cid, "Фото появится в сокром времени!")
        bot.send_message(cid, all_descr[message.text])
        bot.send_message(cid, "Добавить в корзину?", reply_markup=bin_markup)
    elif message.text == "Нет":
        with open(props["users_folder"] + "/" + str(message.from_user.id), "rb") as f:
            usr = json.load(f)
            if usr["prev"] in all_positions:
                for m in menu_categories:
                    if group_list[m].check(usr["prev"]):
                        bot.send_message(
                            cid, "Выберите категорию меню", reply_markup=group_markup
                        )
                        return
            elif usr["prev"] == "Корзина" or usr["prev"] == "Да":
                bot.send_message(cid, "Проверьте, что в корзине все верно")
                bot.send_message(cid, form_bin_mes(usr), reply_markup=groupdone_markup)
            else:
                bot.send_message(cid, props["NotFound"], reply_markup=group_markup)
    elif message.text == "Да":
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
        if usr["prev"] in all_positions:
            if not usr["prev"] in usr["bin"]:
                usr["bin"][usr["prev"]] = 0
            usr["bin"][usr["prev"]] += 1
            usr["price"] += all_prices[usr["prev"]]
            bot.send_message(cid, form_bin_mes(usr))
            bot.send_message(cid, "Продолжить покупки?", reply_markup=bin_markup)
        elif usr["prev"] == "Да":
            bot.send_message(cid, "Выберите категорию меню", reply_markup=group_markup)
        else:
            bot.send_message(cid, props["NotFound"], reply_markup=group_markup)
        with open(props["users_folder"] + "/" + str(message.from_user.id), "w") as f:
            json.dump(usr, f)
    elif message.text == "Корзина":
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
            bot.send_message(cid, form_bin_mes(usr))
            bot.send_message(cid, "Продолжить покупки?", reply_markup=bin_markup)
    elif message.text == "Продолжить покупки":
        bot.send_message(cid, "Выберите категорию меню", reply_markup=group_markup)
    elif message.text == "Убрать товар":
        tmp_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
        tmp_markup.add(types.KeyboardButton("Убрать всё"))
        for el in usr["bin"]:
            tmp_markup.add(types.KeyboardButton(el))
        bot.send_message(cid, "Выберите что убрать", reply_markup=tmp_markup)
    elif message.text == "Убрать всё":
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
        usr["price"] = 0
        del usr["bin"]
        usr["bin"] = {}
        with open(props["users_folder"] + "/" + str(message.from_user.id), "w") as f:
            json.dump(usr, f)
    elif message.text == "Всё верно":
        bot.send_message(
            cid, "С собой или доставка на дом?", reply_markup=deliver_markup
        )
    elif message.text == "С собой":
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
        bot.send_message(
            cid,
            "Ваш заказ передан в пекарню, мы напишем Вам, когда она будет готов",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        all_orders[
            form_order(usr, "C собой", orders_id, message.from_user.username)
        ] = cid
        orders_id += 1
        orders_send()
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
            del usr["bin"]
            usr["bin"] = {}
            usr["price"] = 0
        with open(props["users_folder"] + "/" + str(message.from_user.id), "w") as f:
            json.dump(usr, f)
    elif message.text == "Доставка":
        bot.send_message(
            cid, "Введите адрес доставки?", reply_markup=types.ReplyKeyboardRemove()
        )
    elif message.text == props["Password"]:
        bot.send_message(
            cid, "Вы вошли как владелец", reply_markup=types.ReplyKeyboardRemove()
        )
        admin_usres.append(cid)
        admin_ids.append(message.from_user.id)
        orders_send()
    else:
        with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
            usr = json.load(f)
        if usr["prev"] == "Доставка":
            usr["adress"] = message.text
            bot.send_message(
                cid,
                "Ваш заказ передан в пекарню, мы напишем Вам, когда начнем его доставлять",
                reply_markup=types.ReplyKeyboardRemove(),
            )
            all_orders[
                form_order(
                    usr,
                    "C доставкой по адресу:\n",
                    orders_id,
                    message.from_user.username,
                )
                + message.text
            ] = cid
            orders_id += 1
            orders_send()
            del usr["bin"]
            usr["bin"] = {}
            usr["price"] = 0
            with open(
                props["users_folder"] + "/" + str(message.from_user.id), "w"
            ) as f:
                json.dump(usr, f)
        else:
            for m in "Такой категории не существует,\n попробуйте еще раз":
                bot.send_message(cid, m)
    with open(props["users_folder"] + "/" + str(message.from_user.id), "r") as f:
        usr = json.load(f)
        usr["prev"] = message.text
    with open(props["users_folder"] + "/" + str(message.from_user.id), "w") as f:
        json.dump(usr, f)
