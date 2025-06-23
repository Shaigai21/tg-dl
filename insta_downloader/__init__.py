import os
import instaloader


def download_video(url):
    if not url.startswith("https://www.instagram.com/reel/"):
        raise ValueError("Not an Instagram link")
    try:
        loader = instaloader.Instaloader()
        post_id = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, post_id)
        download_folder = "downloads"
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        loader.download_post(post, target=download_folder)
        # remove jpg and json files from download_folder
        for file in os.listdir(download_folder):
            if file.endswith(".jpg") or file.endswith(".json.xz") or file.endswith(".txt"):
                os.remove(f"{download_folder}/{file}")

        video_filename = f"{download_folder}/{post_id}.mp4"
        return video_filename, post.title
    except Exception as e:
        raise NameError("Download error")
