from . import Bot, read_json_file
import os
import json


def create_config():
    """Создание файла конфигурации."""
    props = {}
    config_path = os.path.join(os.getcwd(), "config.json")
    with open(
        config_path,
        "w+",
    ) as f:
        props["TOKEN"] = input("Введите токен бота:\n")
        props["INSTA_CREDS"] = input("Введите реквизиты от аккаунта в Instagram в формате логин:пароль\n")
        props["LOCALE"] = input("Выберите язык:\n")
        if props["LOCALE"] != "en":
            props["LOCALE"] = "ru"
        print(json.dumps(props), file=f)

def main():
    create_config()
    properties = read_json_file("config.json")
    print(properties)
    bot = Bot(properties["TOKEN"], properties["INSTA_CREDS"], properties["LOCALE"])
    bot.run()

if __name__ == "__main__":
    main()
