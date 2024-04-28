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

## Sentence Transformerでのベクトル検索結果(音声中の文章)
抽出した文章で類似文章を検索してみる。  
idは文章番号。  

```
# 検索結果1
検索対象(id=30): 続いて LDKに向かいますがその途中に飛びらがあり
 検索結果(id=30) rank:1 score:9.61 text:続いて LDKに向かいますがその途中に飛びらがあり
 検索結果(id=36) rank:2 score:8.09 text:では LDKに入っていきましょう
 検索結果(id=38) rank:3 score:5.53 text:こちらの LDK24上を有に超える大空間で

# 検索結果2
検索対象(id=44): こうやってソファーに座るとももちろん
 検索結果(id=44) rank:1 score:12.46 text:こうやってソファーに座るとももちろん
 検索結果(id=21) rank:2 score:8.35 text:すごくすがすがしいお部屋です
 検索結果(id=23) rank:3 score:7.73 text:こちらの部屋からも抜けた景色と緑が見えて気持ちがいいですし

# 検索結果3
検索対象(id=7): 周辺に 高大な力地の広がる
 検索結果(id=7) rank:1 score:8.62 text:周辺に 高大な力地の広がる
 検索結果(id=81) rank:2 score:6.66 text:この目の前に広がる緑と青空
 検索結果(id=22) rank:3 score:5.87 text:そして こちらがなんと12城という広さの要質です

# 検索結果4
検索対象(id=50): そして対面式のオープンキッチンですね
 検索結果(id=50) rank:1 score:19.39 text:そして対面式のオープンキッチンですね
 検索結果(id=62) rank:2 score:12.84 text:キッチンから水周りへと繋がる同線ですね
 検索結果(id=26) rank:3 score:8.41 text:さらに こちらなんとも広いクインクローゼットがありました
```

検索結果2が若干微妙だけど、まぁまぁ同じような文章が検索できていることがわかる。  

## Sentence Transformerでのベクトル検索結果(任意の文章)
任意の文章でRAGで検索してみる。  

```
# 検索結果1
質問:トイレの特徴は？
 検索結果(id=34) rank:1 score:6.8 start:146.38 end:151.48 text:そして こちらにタンクレスで手洗いカウンター付き
 検索結果(id=86) rank:2 score:5.85 start:323.38 end:326.38 text:もちろんペット化物件ですから
 検索結果(id=62) rank:3 score:5.78 start:255.28 end:259.38 text:キッチンから水周りへと繋がる同線ですね

# 検索結果2
質問:間取りは？
 検索結果(id=77) rank:1 score:5.26 start:300.18 end:301.48 text:いやー
 検索結果(id=16) rank:2 score:5.06 start:65.98 end:68.48 text:では上がりましょう
 検索結果(id=78) rank:3 score:4.87 start:301.48 end:302.48 text:これはね

# 検索結果3
質問:どの辺りの地域の物件？
 検索結果(id=88) rank:1 score:6.27 start:329.38 end:333.38 text:最高の住環境ですね
 検索結果(id=3) rank:2 score:6.11 start:12.2 end:15.7 text:今回ご紹介するのは こちらのマンション
 検索結果(id=4) rank:3 score:5.86 start:15.7 end:20.0 text:パークシティ 成長ビートの リノベーションズミ

# 検索結果4
質問:キッチンの広さは？
 検索結果(id=50) rank:1 score:15.54 start:210.58 end:215.38 text:そして対面式のオープンキッチンですね
 検索結果(id=62) rank:2 score:13.12 start:255.28 end:259.38 text:キッチンから水周りへと繋がる同線ですね
 検索結果(id=26) rank:3 score:10.4 start:111.08 end:120.58 text:さらに こちらなんとも広いクインクローゼットがありました

# 検索結果5
質問:バスルームの情報が知りたいです。
 検索結果(id=34) rank:1 score:10.64 start:146.38 end:151.48 text:そして こちらにタンクレスで手洗いカウンター付き
 検索結果(id=62) rank:2 score:8.58 start:255.28 end:259.38 text:キッチンから水周りへと繋がる同線ですね
 検索結果(id=13) rank:3 score:7.83 start:52.58 end:59.18 text:ゆかから天井までの たっぷりとした容量のシューズクローゼットがあります

# 検索結果6
質問:お風呂の情報が知りたいです。
 検索結果(id=34) rank:1 score:9.35 start:146.38 end:151.48 text:そして こちらにタンクレスで手洗いカウンター付き
 検索結果(id=62) rank:2 score:7.19 start:255.28 end:259.38 text:キッチンから水周りへと繋がる同線ですね
 検索結果(id=50) rank:3 score:5.61 start:210.58 end:215.38 text:そして対面式のオープンキッチンですね

# 検索結果7
質問:和室はありますか？
 検索結果(id=21) rank:1 score:7.45 start:84.18 end:87.18 text:すごくすがすがしいお部屋です
 検索結果(id=12) rank:2 score:7.09 start:48.8 end:52.48 text:さあ こちらのエントランスホール まず ここに
 検索結果(id=3) rank:3 score:6.82 start:12.2 end:15.7 text:今回ご紹介するのは こちらのマンション
```

全体的にいまいちだなぁ。  
