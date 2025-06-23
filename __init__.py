import json
from typing import Any
import telebot

def read_json_file(file_path: str):
    """
    Читает и возвращает данные из JSON-файла.

    Параметры:
        file_path (str): Путь к JSON-файлу

    Возвращает:
        Any | None: Данные из файла в формате Python или None при ошибке
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
            
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: JSON file '{file_path}' corrupted.")
    except UnicodeDecodeError:
        print(f"Error: wrong file encoding '{file_path}'.")
    except Exception as e:
        print(f"Error {e}")
    
    return None



class Bot:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)
        self.register_handlers()

    def start(self, message):
        """Обработчик команды /start"""
        self.bot.reply_to(
            message,
            "Привет! Отправь мне ссылку на YouTube Shorts, и я скачаю видео для тебя, чтобы ты мог отправить его)"
        )

    def register_handlers(self):
        """Регистрируем все обработчики"""
        self.bot.message_handler(commands=['start'])(self.start)

    def run(self):
        """Запуск бота"""
        print("Бот запущен...")
        self.bot.polling(none_stop=True)
