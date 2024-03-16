# coding=utf-8
import pathlib
from youtube_utils import download_movie_from_youtube


def main():
    base_path = pathlib.Path(__file__).resolve().parents[1]
    print(base_path)
    download_movie_from_youtube(
        video_url='https://www.youtube.com/watch?v=XgjO95qd_tM',
        save_video_path=str(base_path / 'data' / 'movie' / 'XgjO95qd_tM.mp4'),
        download_resolution = 720,
    )

if __name__ == '__main__':
    main()
