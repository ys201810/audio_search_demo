# audio_search_demo
youtubeから音声をダウンロードし、テキスト化してRAGにて音声検索を行う。  

# how to use
```
$ cd audio_search_demo
$ poetry run python --------
```

## TODO
- [x] youtubeから動画をダウンロード
- [ ] 動画から音声を抽出
- [ ] wisperを利用して音声をテキスト化
- [ ] 学習済みモデルでテキストをエンべディング
- [ ] RAGで音声検索
- [ ] 検出した時刻で動画を切り取る 