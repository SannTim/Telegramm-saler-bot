"""
Модуль работы телеграмм бота
с клиентом и продавцом
"""
import pathlib
import telebot
from telebot import types
import json
import os
import time
from tgsaler import bd_worker
import os

db_controller = bd_worker.db_controller
try:
    with open(os.path.dirname(os.path.abspath(__file__)) + "/config.json") as f:
        props = json.load(f)
except Exception:
    print("You need to create config file first")
    print("run command: tgsalerconfig")
    exit


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
menu_catigories = []



def update_markups():
    """
    Функция обновления обновления клавиатурной разметки.
    """

    global group_markup, groupdone_markup, deliver_markup, bin_markup, group_list
    tmp_menu_categories = [(i[0], i[1]) for i in bd.get_categories()]
    # print(tmp_menu_categories)
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
    group_list = {}
    for gr in tmp_menu_categories:
        opend_group = bd.get_all_by_category(gr[0])
        group_list[gr[1]] = group(opend_group)
        group_markup.add(types.KeyboardButton(gr[1]))
    del tmp_menu_categories


def updater():
    """
    Функция, вызывающая функцию update_markups() каждые 10 секунд.
    """

    while True:
        update_markups()
        time.sleep(10)


def orders_send():
    """
    Функция отправления сообщения с заказами администраторам.
    """

    orders_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    msg = "\n".join(all_orders)
    if len(all_orders) == 0:
        return
    for el in all_orders:
        orders_markup.add(types.KeyboardButton(str(el[0])))
    for admin in admin_usres:
        bot.send_message(admin, msg)
        bot.send_message(admin, "Какой заказ готов?")


def form_bin_mes(usr):
    """
    Формирует текст для корзины пользователя.

    Args:
        usr (dict): Информация о пользователе и его корзине.

    Returns:
        str: Текст с информацией о корзине пользователя.
    """

    ans = "В вашей корзине сейчас:\n"
    for el in usr["bin"]:
        if usr["bin"][el] != 1:
            ans += "x" + str(usr["bin"][el]) + ": "
        ans += el + "\n"
    ans += "Сумма:" + str(usr["price"])
    return ans


def form_order(usr, st, id, name):
    """
    Формирует текст заказа для пользователя.

    Args:
        usr (dict): Информация о пользователе и его корзине.
        st (str): Статус заказа.
        id (int): Уникальный идентификатор заказа.
        name (str): Имя пользователя.

    Returns:
        str: Текст заказа для пользователя.
    """

    # print(id)
    ans = str(id) + " заказ:\n"
    ans += "От пользователя: @" + name + "\n"
    for el in usr["bin"]:
        if usr["bin"][el] != 1:
            ans += "x" + str(usr["bin"][el]) + ": "
        ans += el + "\n"
    ans += "На сумму:" + str(usr["price"]) + "\n" + st
    return ans


def get_usr_byid(id):
    return bd.get_user_by_id(id)


def save_user_data(data):
    bd.edit_user_by_data(data)


class group:
    """
    Класс, представляющий группу товаров.

    Attributes:
        markup (telebot.types.ReplyKeyboardMarkup): Маркап клавиатуры.
        positions (list): Список позиций товаров в группе.

    Methods:
        check(x): Проверяет наличие товара в группе.
        markup(): Возвращает маркап клавиатуры для группы.
    """

    def __init__(self, group_data):
        """
        Инициализирует группу товаров.

        Args:
            group_data (list): Список данных о товарах в группе.
        """

        global all_positions
        self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.markup.add(types.KeyboardButton("Назад"))
        self.markup.add(types.KeyboardButton("Корзина"))
        self.positions = []
        for el in group_data:
            # print(el)
            new_name = el["name"] + ", " + str(el["price"]) + " " + el["currency"]
            self.positions.append(new_name)
            all_descr[new_name] = el["descr"]
            all_prices[new_name] = el["price"]
            all_images[new_name] = el["photo"]

        for el in self.positions:
            self.markup.add(types.KeyboardButton(el))
        all_positions = all_positions + self.positions

    def check(self, x):
        """
        Проверяет наличие товара в группе.

        Args:
            x (str): Наименование товара.

        Returns:
            bool: Результат проверки.
        """

        return x in self.positions

    def markup(self):
        """
        Возвращает маркап клавиатуры для группы.

        Returns:
            telebot.types.ReplyKeyboardMarkup: Маркап клавиатуры.
        """

        return self.markup


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """
    Отправляет приветственные сообщения при командах /start и /help.

    Args:
        message (telebot.types.Message): Сообщение от пользователя.
    """
    global bd
    cid = message.chat.id
    bd.add_user(tgid=f"{message.from_user.id}")
    sti = open(
        os.path.dirname(os.path.abspath(__file__)) + "/stikers/AnimatedSticker.tgs",
        "rb",
    )
    bot.send_sticker(cid, sti)
    for m in props["Welcome messages"]:
        bot.send_message(cid, m)
    bot.send_message(cid, "Выберите категорию меню", reply_markup=group_markup)


@bot.message_handler(content_types="text")
def category_go(message):
    """
    Обрабатывает сообщения пользователя и реагирует на них.

    Args:
        message (telebot.types.Message): Сообщение от пользователя.
    """
    global orders_id, menu_catigories, bd
    # print(message.from_user)
    if message.from_user.id in admin_ids:

        for el in all_orders:
            # print(el[: len(message.text)])
            # print(message.text)
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
    if message.text in menu_catigories:
        bot.send_message(
            cid,
            "Выберите продукт из группы",
            reply_markup=group_list[message.text].markup,
        )
    elif message.text == "Назад":
        bot.send_message(cid, "Выберите категорию меню",
                         reply_markup=group_markup)
    elif message.text in all_positions:
        usr = get_usr_byid(message.from_user.id)
        if usr["prev"] == "Убрать товар":
            usr["price"] -= usr["bin"][message.text] * all_prices[message.text]
            del usr["bin"][message.text]

            save_user_data(usr)
            bot.send_message(cid, "Проверьте, что в корзине все верно")
            bot.send_message(cid, form_bin_mes(
                usr), reply_markup=groupdone_markup)
            return
        prod = bd.get_product_data(",".join(message.text.split(",")[:-1]))
        # print(prod)
        try:
            im = open("images/" + prod["photo"], "rb")
            bot.send_photo(cid, im)
        except Exception:
            bot.send_message(cid, "Фото появится в сокром времени!")
        if all_descr[message.text]:
            bot.send_message(cid, all_descr[message.text])
        else:
            bot.send_message(cid, "Описание появится в скором времени")
        bot.send_message(cid, "Добавить в корзину?", reply_markup=bin_markup)
    elif message.text == "Нет":
        usr = get_usr_byid(message.from_user.id)
        if usr["prev"] in all_positions:
            for m in menu_catigories:
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
        usr = get_usr_byid(message.from_user.id)
        if usr["prev"] in all_positions:
            if not usr["prev"] in usr["bin"]:
                usr["bin"][usr["prev"]] = 0
            usr["bin"][usr["prev"]] += 1
            usr["price"] += all_prices[usr["prev"]]
            bot.send_message(cid, form_bin_mes(usr))
            bot.send_message(cid, "Продолжить покупки?",
                             reply_markup=bin_markup)
        elif usr["prev"] == "Да":
            bot.send_message(cid, "Выберите категорию меню",
                             reply_markup=group_markup)
        else:
            bot.send_message(cid, props["NotFound"], reply_markup=group_markup)
        save_user_data(usr)
    elif message.text == "Корзина":
        usr = get_usr_byid(message.from_user.id)
        bot.send_message(cid, form_bin_mes(usr))
        bot.send_message(cid, "Продолжить покупки?", reply_markup=bin_markup)
    elif message.text == "Продолжить покупки":
        bot.send_message(cid, "Выберите категорию меню",
                         reply_markup=group_markup)
    elif message.text == "Убрать товар":
        tmp_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        usr = get_usr_byid(message.from_user.id)
        tmp_markup.add(types.KeyboardButton("Убрать всё"))
        for el in usr["bin"]:
            tmp_markup.add(types.KeyboardButton(el))
        bot.send_message(cid, "Выберите что убрать", reply_markup=tmp_markup)
    elif message.text == "Убрать всё":
        usr = get_usr_byid(message.from_user.id)
        usr["price"] = 0
        usr["bin"] = {}
        save_user_data(usr)
    elif message.text == "Всё верно":
        bot.send_message(
            cid, "С собой или доставка на дом?", reply_markup=deliver_markup
        )
    elif message.text == "С собой":
        usr = get_usr_byid(message.from_user.id)
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
        usr = get_usr_byid(message.from_user.id)
        del usr["bin"]
        usr["bin"] = {}
        usr["price"] = 0
        save_user_data(usr)
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
        usr = get_usr_byid(message.from_user.id)
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
            save_user_data(usr)
        else:
            for m in "Такой категории не существует,\n попробуйте еще раз":
                bot.send_message(cid, m)

    usr = get_usr_byid(message.from_user.id)
    usr["prev"] = message.text
    save_user_data(usr)
