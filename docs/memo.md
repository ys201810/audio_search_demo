# メモ
## 1. youtubeの動画をダウンロード
extract_movie_from_youtube.pyの以下の箇所。
```
    download_movie_from_youtube(
        video_url='https://www.youtube.com/watch?v=XgjO95qd_tM',
        download_resolution=720,
        save_video_path=str(base_path / 'data' / 'movie' / 'XgjO95qd_tM.mp4')
    )
```

