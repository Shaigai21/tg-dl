import json
import telebot
import os
from video_downloader_bot.insta_downloader import download_video as insta_download
from video_downloader_bot.tiktak_downloader import download_video as tiktak_download
from video_downloader_bot.youtube_downloader import download_video as youtube_download


def _(text):
    return text


def read_json_file(file_path: str):
    """
    Читает и возвращает данные из JSON-файла.
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
            _("Привет! Отправь мне ссылку на YouTube Shorts, Instagram или TikTok, и я скачаю видео для тебя.")
        )

    def handle_video_links(self, message):
        """Обработчик ссылок на видео"""
        url = message.text.strip()

        # Определение сервиса
        if 'youtube.com' in url or 'youtu.be' in url:
            service = "YouTube"
            download_func = youtube_download
        elif 'instagram.com' in url:
            service = "Instagram"
            download_func = insta_download
        elif 'tiktok.com' in url:
            service = "TikTok"
            download_func = tiktak_download
        else:
            # Только в личных — отправляем ответ об ошибке
            if message.chat.type == 'private':
                self.bot.reply_to(message, _("❌ Неподдерживаемый сервис. Отправьте ссылку YouTube, Instagram или TikTok."))
            return

        status_msg = None

        # Только в ЛС показываем "Скачиваем..."
        if message.chat.type == 'private':
            status_msg = self.bot.reply_to(message, _(f"⏳ Скачиваем видео с {service}..."))

        try:
            video_path, video_name = download_func(url)

            if not video_path or not os.path.exists(video_path):
                raise FileNotFoundError(_("При загрузке произошла ошибка. Проверьте корректность ссылки и повторите."))

            with open(video_path, 'rb') as video_file:
                self.bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption=video_name if message.chat.type == 'private' else None,
                    reply_to_message_id=message.message_id
                )

            os.remove(video_path)

            if status_msg:
                self.bot.delete_message(status_msg.chat.id, status_msg.message_id)

        except Exception as e:
            if message.chat.type == 'private':
                error_msg = _(f"❌ Ошибка при загрузке видео: {str(e)}")
                if status_msg:
                    self.bot.edit_message_text(
                        chat_id=status_msg.chat.id,
                        message_id=status_msg.message_id,
                        text=error_msg
                    )
                else:
                    self.bot.reply_to(message, error_msg)
            else:
                print(f"[ERROR in group] {e}")

    def register_handlers(self):
        """Регистрируем все обработчики"""
        self.bot.message_handler(commands=['start'])(self.start)

        # Обрабатываем текст только если это потенциальная ссылка на видео
        @self.bot.message_handler(func=lambda message: message.content_type == 'text')
        def message_filter(message):
            if any(domain in message.text.lower() for domain in ['youtube.com', 'youtu.be', 'tiktok.com', 'instagram.com']):
                self.handle_video_links(message)

    def run(self):
        """Запуск бота"""
        print("Бот запущен...")
        self.bot.polling(none_stop=True)


# Пример запуска
if __name__ == '__main__':
    token = os.getenv("BOT_TOKEN")  # Убедитесь, что переменная окружения установлена
    if not token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
    else:
        bot = Bot(token)
        bot.run()
