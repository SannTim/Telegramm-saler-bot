# Telegramm-saler-bot

## Предназначение
Данная программа позволяет установить и запустить Телеграмм бота, который позволяет покупателю легко покупать товары, а продавцу их продавать
## Функционал
Есть три группы людей, которые будут ползоваться ботом, с своим Функционалом:
- покупатели
- продавцы
- администраторы
### Функционал пользователя
- [X] возможность преехода по категориям продуктов
- [X] возможность добавления продукта в корзину
- [X] возможность заказа выбранных продуктов
    - [X] выбор способа получения (доставка или самовывоз)
        - [X] возможность указания адресса доставки
- [X] возможность связи с продавцом по поводу заказа
### Функционал продавца
- [X] получение уведомления при заказе нового продукта
- [X] изменение статуса заказа
- [X] возможность связи с пользователем по поводу заказа
### Функционал администратора
- [X] добавление нового продукта через cmd в базу данных
- [X] изменение уже существующего продукта
- [X] удаление существующего продукта
## Дополнительный Функционал
- [X] работа с базой данных
- [-] возможность выбора языка в config файле
    - [ ] возможность выбора языка в cmd администратора


# Требования к проекту
- [X] Все стадии сборки проекта должны воспроизводиться любым желающим
- [X] В котором flake8 (или pylint), а также pydocstyle не находят ошибок
- [X] В котором есть немножко тестов
- [ ] В котором есть немножко документации
- [X] В котором есть немножко локализации с использованием babel
- [ ] В котором есть немножко автоматизации сборки / деплоймента
