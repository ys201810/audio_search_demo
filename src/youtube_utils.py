# coding=utf-8
from yt_dlp import YoutubeDL


def download_movie_from_youtube(video_url: str, save_video_path: str, download_resolution: int=720):
    ydl_opts = {
        'format': f'best[height<={download_resolution}]',
        'overwrites': True,
        'outtmpl': save_video_path
    }
    # youtubeからの動画ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

