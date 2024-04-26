# coding=utf-8
import pathlib
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
import whisper
import time


def download_movie_from_youtube(video_url: str, save_video_file: pathlib.Path, download_resolution: int=720):
    if save_video_file.exists():
        print(f'File already exists: {save_video_file}')
        return False
    ydl_opts = {
        'format': f'best[height<={download_resolution}]',
        'overwrites': True,
        'outtmpl': str(save_video_file)
    }
    # youtubeからの動画ダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])


def extruct_audio_from_movie(save_video_file: pathlib.Path, save_audio_file: pathlib.Path, codec :str="pcm_s32le"):
    if save_audio_file.exists():
        print(f'File already exists: {save_audio_file}')
        return False
    clip = VideoFileClip(str(save_video_file))
    clip.audio.write_audiofile(str(save_audio_file), codec=codec)


def extract_text_from_audio(save_audio_file: pathlib.Path, save_text_file: pathlib.Path):
    # whisperでの文字抽出
    model = whisper.load_model("base")

    wisper_start = time.time()
    result = model.transcribe(str(save_audio_file), verbose=True)
    wisper_end = time.time()
    print(f"実行時間:{round(wisper_end - wisper_start, 5)}'s")

    with open (save_text_file, 'w') as f:
        f.write('\t'.join(['id', 'start', 'end', 'text']) + '\n')
        for value in result["segments"]:
            f.write(
                '\t'.join(
                    [
                        str(value['id']),
                        str(round(value['start'], 2)),
                        str(round(value['end'], 2)),
                        value['text']
                    ]
                )
                + '\n'
            )
