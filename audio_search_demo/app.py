# coding=utf-8
"""
youtube動画IDとクエリテキストを入力して、指定時間から動画を再生
"""
import settings
from pathlib import Path
import streamlit as st
import pyarrow.parquet as pq
from sentence_embedder import SentenceEmbedder
from qdrant_manager import QdrantManager


def main():
    base_path = Path(__file__).resolve().parents[1]
    st.title('youtube動画IDと検索テキストで、関連するシーンの再生時間から動画を再生')
    youtube_movie_id = st.text_input('youtubeの動画ID', placeholder='動画ID', max_chars=11, help='youtubeのULR：https://www.youtube.com/watch?v=9dA252nFHs8の「9dA252nFHs8」の箇所')
    query_text = st.text_input('検索したい文章', placeholder='テキストを何でも入れてね', max_chars=100, help='youtubeのULR：https://www.youtube.com/watch?v=9dA252nFHs8の「9dA252nFHs8」の箇所')
    BASE_VIDEO_URL = settings.BASE_VIDEO_URL

    if st.button('テキストを検索'):
        parquet_file_path = base_path / 'data' / 'text'
        target_names = [val.stem for val in list(parquet_file_path.glob('*.parquet'))]
        if youtube_movie_id not in target_names:
            st.write(f'{youtube_movie_id}は扱えません。make_embeddings_db.pyでRAGに必要な情報を作成してください。')
        else:
            parquet_file = base_path / 'data' / 'text' / f'{youtube_movie_id}.parquet'
            if parquet_file.exists():
                table_loaded = pq.read_table(parquet_file)
                df_text = table_loaded.to_pandas()
                EMBEDDING_MODEL = settings.EMBEDDING_MODEL
                sentence_embedder = SentenceEmbedder(EMBEDDING_MODEL)
                embedding_vectors = sentence_embedder.get_embedding_vector([query_text])
                QDRANT_URL = settings.QDRANT_URL
                qdrant_manager = QdrantManager(url=QDRANT_URL, collection_name=youtube_movie_id)
                search_results = qdrant_manager.search_vectors(vector=embedding_vectors[0], top_k=1)

                text = df_text.query(f'id == {search_results[0].id}').text.item()
                start = df_text.query(f'id == {search_results[0].id}')['start'].item()
                score = round(search_results[0].score, 2)
                st.markdown('### 質問文のRAG検索結果')
                st.markdown(f'スコア:{score} 開始時間:{start} テキスト:{text}')

                st.video(
                    data=f'{BASE_VIDEO_URL}{youtube_movie_id}',
                    format='video/mp4',
                    start_time=start,
                )

if __name__ == '__main__':
    main()
