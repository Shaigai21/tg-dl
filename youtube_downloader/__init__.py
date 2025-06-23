import yt_dlp
import os


def download_video(url):
    """
    Функция для скачивания видео с ссылки на ютуб
    Скачивание происходит в папку downloads
    Функция возвращает путь к видео и его название
    """
    print("скачиваю", url)
    if (
        not url.startswith("https://www.youtube.com/shorts")
        and not url.startswith("https://www.youtube.com/watch?")
        and not url.startswith("https://youtube.com/shorts")
        and not url.startswith("https://youtube.com/watch?")
    ):
        raise ValueError("Not youtube link")
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
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get("title", "video")
            video_filename = ydl.prepare_filename(info_dict)

    except Exception:
        raise NameError("Download error")

    return video_filename, video_title
