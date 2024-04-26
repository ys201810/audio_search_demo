# coding=utf-8
import pathlib
import settings
from audio_search_utils import download_movie_from_youtube, extruct_audio_from_movie, extract_text_from_audio
import embedding_text
import pandas as pd


def main():
    base_path = pathlib.Path(__file__).resolve().parents[1]
    MOVIE_NAME = settings.MOVIE_NAME
    BASE_VIDEO_URL = settings.BASE_VIDEO_URL

    # download movie from YouTube
    save_video_file = base_path / 'data' / 'movie' / f'{MOVIE_NAME}.mp4'
    if not save_video_file.exists():
        video_url = BASE_VIDEO_URL + MOVIE_NAME
        download_movie_from_youtube(
            video_url=video_url,
            save_video_file=save_video_file,
            download_resolution=720,
        )
    else:
        print(f'{save_video_file.name} is already download')

    # extract audio from movie
    save_audio_file = base_path / 'data' / 'audio' / f'{MOVIE_NAME}.wav'
    if not save_audio_file.exists():
        extruct_audio_from_movie(save_video_file, save_audio_file)
    else:
        print(f'{save_audio_file.name} is already extracted')

    # extract text from audio
    save_text_file = base_path / 'data' / 'text' / f'{MOVIE_NAME}.tsv'
    if not save_text_file.exists():
        extract_text_from_audio(save_video_file, save_text_file)
        text_df = pd.read_csv(save_text_file, sep='\t')
    else:
        print(f'{save_text_file.name} is already extracted')
        text_df = pd.read_csv(save_text_file, sep='\t')

    # text embedding
    EMBEDDING_MODEL = settings.EMBEDDING_MODEL
    embeddings = embedding_text.run(EMBEDDING_MODEL, text_df['text'].to_list()[:3])


if __name__ == '__main__':
    main()