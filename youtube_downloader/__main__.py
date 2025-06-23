from . import download_video

rickroll = "https://www.youtube.com/watch?v=xvFZjo5PgG0"

print(rickroll.startswith("https://youtube.com/watch?"))


print(download_video(rickroll))
