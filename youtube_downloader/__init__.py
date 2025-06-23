import yt_dlp
import os


def download_video(url):
    print("скачиваю", url)
    if (not url.startswith("https://www.youtube.com/shorts") and
    not url.startswith("https://www.youtube.com/watch?") and
    not url.startswith("https://youtube.com/shorts") and
    not url.startswith("https://youtube.com/watch?")):
        raise ValueError("Not youtube link")
    try:
        # Папка для загрузки
        download_folder = "downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Настройки для yt-dlp
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'retries': 20,
            'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            video_filename = ydl.prepare_filename(info_dict)

    except Exception as e:
        raise NameError("Download error")

    return video_filename, video_title
