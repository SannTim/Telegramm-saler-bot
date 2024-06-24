import os
import json

def create_config(): 
    props = {}
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__),  "../tgsaler/config.json"), "w")) as f:
        props["token"] = input("Введите токен бота:\n")
        props["Password"] = input("Введите пароль администратора:\n")
        mes = input("Введите приветственные сообщение(конец --- пустая строка):\n")
        props["Welcome messages"] = []
        props["Welcome messages"].append(mes)
        while mes := input():
            props["Welcome messages"].append(mes)
        props["NotFound"] = input(
            "Введите сообщение если был введен несуществующий товар:\n"
        )
        print(json.dumps(props), file=f)
