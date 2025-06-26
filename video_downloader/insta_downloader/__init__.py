import os
import instaloader
import logging


def download_video(url, creds=None):
    """
    Функция для скачивания видео с ссылки instagram.

    Есть возможность программного входа в аккаунт
    Скачивание происходит в папку tg_dl_downloads
    Функция возвращает путь к видео и его название
    """
    print("скачиваю", url)
    if not url.startswith("https://www.instagram.com/reel"):
        raise ValueError("Not an Instagram Reels link")

    try:
        logging.getLogger("instaloader").setLevel(logging.CRITICAL)

        class CustomInstaloader(instaloader.Instaloader):
            def format_filename(self, post, target=None):
                return f"{post.shortcode}"

        loader = CustomInstaloader(
            download_pictures=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            quiet=True,
            filename_pattern="{shortcode}"
        )
        # Авторизация, если переданы логин и пароль
        if creds:
            username, password = creds.split(":")
            if username and password:
                loader.login(username, password)
            else:
                print("Username and password are not in provided format.")
        else:
            print("Username and password are required for login.")
            print("Working without login")

        # Получение короткого кода поста
        post_id = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, post_id)

        # Создание папки для загрузок
        download_folder = "tg_dl_downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Загрузка поста
        loader.download_post(post, target=download_folder)

        # Удаление ненужных файлов
        for file in os.listdir(download_folder):
            if (
                file.endswith(".jpg")
                or file.endswith(".json.xz")
                or file.endswith(".txt")
            ):
                os.remove(os.path.join(download_folder, file))

        # Формирование имени видеофайла
        video_filename = os.path.join(download_folder, f"{post_id}.mp4")
        return video_filename, post.title

    except instaloader.exceptions.BadCredentialsException:
        raise RuntimeError("Invalid Instagram credentials.")
    except instaloader.exceptions.ConnectionException:
        raise RuntimeError("Connection error while accessing Instagram.")
    except Exception as e:
        raise RuntimeError(f"Download error: {e}")
