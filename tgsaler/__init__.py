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

