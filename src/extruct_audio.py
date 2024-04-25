# coding=utf-8
import pathlib
from audio_search_utils import download_movie_from_youtube, extruct_audio
import whisper
import time
import pickle


def main():
    base_path = pathlib.Path(__file__).resolve().parents[1]
    movie_name = '9dA252nFHs8'
    video_url = 'https://www.youtube.com/watch?v=' + movie_name
    save_video_path = base_path / 'data' / 'movie' / f'{movie_name}.mp4'
    save_audio_path = base_path / 'data' / 'audio' / f'{movie_name}.wav'
    save_text_path = base_path / 'data' / 'text' / f'{movie_name}.pkl'

    download_movie_from_youtube(
        video_url=video_url,
        save_video_path=save_video_path,
        download_resolution = 720,
    )

    # audioの抽出
    extruct_audio(save_video_path, save_audio_path)

    # whisperでの文字抽出
    model = whisper.load_model("base")

    wisper_start = time.time()
    result = model.transcribe(str(save_audio_path), verbose=True)
    wisper_end = time.time()
    print(f"実行時間:{round(wisper_end - wisper_start, 5)}'s")

    with open (save_text_path, 'w') as f:
        f.write(result["segments"])


if __name__ == '__main__':
    main()
