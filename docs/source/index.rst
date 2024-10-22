.. Telegramm-saler-bot documentation master file
   Created by sphinx-quickstart on Sat Jun 8 2024.
   You are free to customize this file to your preferences, but it should at least
   contain the root `toctree` directive.

Welcome to Telegramm-saler-bot's Documentation
==============================================

Telegramm-saler-bot
-------------------
Telegramm-saler-bot предназначен для установки и запуска Telegram-бота, упрощающего процесс покупки и продажи товаров. Бот позволяет покупателям легко приобретать товары, а продавцам - осуществлять продажи.

Функционал
----------
Программа предоставляет функциональные возможности для трех групп пользователей:
- Покупатели
- Продавцы
- Администраторы

Функционал пользователя
~~~~~~~~~~~~~~~~~~~~~~~
- [X] Просмотр категорий продуктов
- [X] Добавление продуктов в корзину
- [X] Оформление заказов
- [X] Выбор способа получения (доставка или самовывоз)
- [X] Указание адреса для доставки
- [X] Связь с продавцом относительно заказа

Функционал продавца
~~~~~~~~~~~~~~~~~~~
- [X] Получение уведомлений о новых заказах
- [X] Изменение статуса заказа
- [X] Взаимодействие с покупателями относительно заказов

Функционал администратора
~~~~~~~~~~~~~~~~~~~~~~~~~
- [X] Добавление новых товаров через командную строку в базу данных
- [X] Изменение существующих товаров
- [X] Удаление существующих товаров

Дополнительный функционал
~~~~~~~~~~~~~~~~~~~~~~~~~~
- [X] Работа с базой данных
- [-] Возможность выбора языка в файле конфигурации
   - [X] Возможность выбора языка в командной строке администратора

Требования к проекту
---------------------
- [X] Все этапы сборки проекта должны быть воспроизводимы любым желающим
- [X] Отсутствие ошибок при использовании flake8 (или pylint) и pydocstyle
- [X] Наличие базового уровня тестов
- [X] Присутствие базового уровня документации
- [X] Наличие частичной локализации с использованием babel
- [X] Присутствие базового уровня автоматизации сборки / развертывания

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   tgsaler
   bd_worker
   bd_console
   setuper

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`