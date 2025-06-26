import gettext
from unittest.mock import MagicMock
from video_downloader.insta_downloader import download_video as insta_download
from video_downloader.youtube_downloader import download_video as youtube_download
import unittest
from video_downloader import Bot


def empty_func(*args):
    pass


class Test_link_check(unittest.TestCase):
    def test_link_insta_right(self):
        try:
            insta_download("https://www.instagram.com/reels/DHyddMqtN9U/?next=%2F")
        except Exception as e:
            self.assertNotEqual(str(e), str(ValueError("Not an Instagram Reels link")))

    def test_link_insta_false(self):
        try:
            insta_download("https://www.outstagram.com/reel/GOOOOOAL")
        except Exception as e:
            self.assertEqual(str(e), str(ValueError("Not an Instagram Reels link")))

    def test_link_youtube_false(self):
        try:
            youtube_download("https://www.Itube.com/shorts/xaxaxax")
        except Exception as e:
            self.assertEqual(str(e), str(ValueError("Not youtube link")))

    def test_link_youtube_right(self):
        try:
            youtube_download("https://www.youtube.com/watch?v=j1B_ScRYU4I")
        except Exception as e:
            self.assertNotEqual(str(e), str(ValueError("Not youtube link")))


LOCALES = {
    "ru": gettext.NullTranslations(),
}


def _(*args):
    return LOCALES["ru"].gettext(*args)


class Test_bot(unittest.TestCase):
    def setUp(self) -> None:
        self.res = None
        self.Bot = Bot.__new__(Bot)
        self.Bot.bot = MagicMock()
        self.Bot._ = _
        self.Bot.bot.reply_to = lambda y, x: setattr(self, "res", x)
        return super().setUp()

    def test_start(self):
        self.Bot.start(None)
        self.assertEqual(
            "Привет! Отправь мне ссылку на YouTube Shorts, Instagram или TikTok, и я скачаю видео для тебя.",
            self.res,
        )

    def test_filter_false(self):
        class fakemessage:
            text = "https://loltube.com/bruh"
            chat = MagicMock()
            chat.type = "private"

        self.Bot.handle_video_links(fakemessage())
        self.assertEqual(
            "❌ Неподдерживаемый сервис. Отправьте ссылку YouTube, Instagram или TikTok.",
            self.res,
        )

    def test_filter_true(self):
        class fakemessage:
            text = "https://www.youtube.com/watch?v=j1B_ScRYU4I"
            chat = MagicMock()
            chat.type = "not private"
            self.assertEqual(None, self.res)

        self.Bot.handle_video_links(fakemessage())
        self.assertNotEqual(
            "❌ Неподдерживаемый сервис. Отправьте ссылку YouTube, Instagram или TikTok.",
            self.res,
        )
