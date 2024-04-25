# coding=utf-8
import pathlib
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip


def download_movie_from_youtube(video_url: str, save_video_path: pathlib.Path, download_resolution: int=720):
    if save_video_path.exists():
        print(f'File already exists: {save_video_path}')
        return False
    ydl_opts = {
        'format': f'best[height<={download_resolution}]',
        'overwrites': True,
        'outtmpl': str(save_video_path)
    }
    # youtubeからの動画ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def extruct_audio(save_video_path: pathlib.Path, save_audio_path: pathlib.Path, codec :str="pcm_s32le"):
    if save_audio_path.exists():
        print(f'File already exists: {save_audio_path}')
        return False
    clip = VideoFileClip(str(save_video_path))
    clip.audio.write_audiofile(str(save_audio_path), codec=codec)
