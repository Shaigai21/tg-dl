import gettext
import json
import telebot
import os
from .tiktok_downloader import download_video as tiktok_download
from .insta_downloader import download_video as insta_download
from .youtube_downloader import download_video as youtube_download

locales_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "locales"))

LOCALES = {
    "en": gettext.translation("video_downloader", locales_dir, ["en"]),
    "ru": gettext.NullTranslations(),
}


def read_json_file(file_path: str):
    """Читает и возвращает данные из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
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
    def __init__(self, token: str, insta_creds: str = None, locale: str = "ru"):
        """Инициализирует бота с заданным токеном и регистрирует обработчики."""
        self.bot = telebot.TeleBot(token)
        self.register_handlers()
        self.insta_creds = insta_creds

        def _(*args):
            return LOCALES[locale].gettext(*args)

        self._ = _

    def start(self, message):
        """
        Обработчик команды /start.

        Отвечает приветственным сообщением.
        """
        self.bot.reply_to(
            message,
            self._(
                "Привет! Отправь мне ссылку на YouTube Shorts, Instagram или TikTok, и я скачаю видео для тебя."
            ),
        )

    def handle_video_links(self, message):
        """
        Обрабатывает сообщения с ссылками на видео.

        Определяет платформу, скачивает видео и отправляет его пользователю.
        """
        url = message.text.strip()

        # Определение сервиса
        if "youtube.com" in url or "youtu.be" in url:
            service = "YouTube"
            download_func = youtube_download
        elif "instagram.com" in url:
            service = "Instagram"
            download_func = insta_download
        elif "tiktok.com" in url:
            service = "TikTok"
            download_func = tiktok_download
        else:
            # Только в личных — отправляем ответ об ошибке
            if message.chat.type == "private":
                self.bot.reply_to(
                    message,
                    self._(
                        "❌ Неподдерживаемый сервис. Отправьте ссылку YouTube, Instagram или TikTok."
                    ),
                )
            return

        status_msg = None

        # Только в ЛС показываем "Скачиваем..."
        if message.chat.type == "private":
            status_msg = self.bot.reply_to(
                message,
                self._("⏳ Скачиваем видео с {service}...").format(service=service),
            )

        try:
            if service == "Instagram" and self.insta_creds:
                video_path, video_name = insta_download(url, creds=self.insta_creds)
            else:
                video_path, video_name = download_func(url)

            print(video_path)
            if not video_path or not os.path.exists(video_path):
                raise FileNotFoundError(
                    self._(
                        "При загрузке произошла ошибка. Проверьте корректность ссылки и повторите."
                    )
                )

            with open(video_path, "rb") as video_file:
                self.bot.send_video(
                    chat_id=message.chat.id,
                    video=video_file,
                    caption=video_name if message.chat.type == "private" else None,
                    reply_to_message_id=message.message_id,
                )

            if status_msg:
                self.bot.delete_message(status_msg.chat.id, status_msg.message_id)

        except Exception as e:
            if message.chat.type == "private":
                error_msg = self._(f"❌ Ошибка при загрузке видео: {str(e)}")
                if status_msg:
                    self.bot.edit_message_text(
                        chat_id=status_msg.chat.id,
                        message_id=status_msg.message_id,
                        text=error_msg,
                    )
                else:
                    self.bot.reply_to(message, error_msg)
            else:
                print(f"[ERROR in group] {e}")

    def register_handlers(self):
        """Регистрируем все обработчики."""
        self.bot.message_handler(commands=["start"])(self.start)

        # Обрабатываем текст только если это потенциальная ссылка на видео
        @self.bot.message_handler(func=lambda message: message.content_type == "text")
        def message_filter(message):
            if any(
                domain in message.text.lower()
                for domain in ["youtube.com", "youtu.be", "tiktok.com", "instagram.com"]
            ):
                self.handle_video_links(message)

    def run(self):
        """Запускает бота в режиме постоянного опроса."""
        print("Бот запущен...")
        self.bot.polling(none_stop=True)


# Пример запуска
if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")  # Убедитесь, что переменная окружения установлена
    if not token:
        print("❌ BOT_TOKEN не найден в переменных окружения")
    else:
        bot = Bot(token)
        bot.run()
