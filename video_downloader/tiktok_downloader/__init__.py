import yt_dlp
import os


class QuietLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def download_video(url):
    """
    Функция для скачивания видео с tiktok ссылки.

    Скачивание происходит в папку downloads
    Функция возвращает путь к видео и его название
    """
    try:
        # Папка для загрузки
        download_folder = "tg_dl_downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Настройки для yt-dlp
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "retries": 20,
            "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
            "noplaylist": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "postprocessor_args": [
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-preset",
                "fast",
            ],
            "merge_output_format": "mp4",
            "logger": QuietLogger(),
            "progress_hooks": [lambda d: None],
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", "video")
            video_filename = ydl.prepare_filename(info_dict)

    except Exception:
        raise NameError("Download error")

    return video_filename, video_title
