# coding=utf-8
from pathlib import Path
import settings
from audio_search_utils import download_movie_from_youtube, extruct_audio_from_movie, extract_text_from_audio
from sentence_embedder import SentenceEmbedder
import pandas as pd
from qdrant_manager import QdrantManager
import pyarrow as pa
import pyarrow.parquet as pq


def main():
    base_path = Path(__file__).resolve().parents[1]
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
        df_text = pd.read_csv(save_text_file, sep='\t')
    else:
        print(f'{save_text_file.name} is already extracted')
        df_text = pd.read_csv(save_text_file, sep='\t')

    # text embedding
    QDRANT_URL = settings.QDRANT_URL
    qdrant_manager = QdrantManager(url=QDRANT_URL, collection_name=MOVIE_NAME)

    parquet_file = base_path / 'data' / 'text' / f'{MOVIE_NAME}.parquet'
    if parquet_file.exists():
        table_loaded = pq.read_table(parquet_file)
        df_text = table_loaded.to_pandas()
        vectors = df_text['vector'].to_list()
        print(f'{parquet_file.name}.parquet is already created')
    else:
        EMBEDDING_MODEL = settings.EMBEDDING_MODEL
        sentence_embedder = SentenceEmbedder(model_name=EMBEDDING_MODEL)
        embeddings = sentence_embedder.get_embedding_vector(EMBEDDING_MODEL, df_text['text'].to_list())
        df_text['vector'] = pd.Series(embeddings.tolist())
        table = pa.Table.from_pandas(df_text)
        pq.write_table(table, parquet_file)

        # save embeddings
        EMBEDDING_DIM = settings.EMBEDDING_DIM
        qdrant_manager.create_collection(dim=EMBEDDING_DIM)
        ids = df_text['id'].to_list()
        vectors = df_text['vector'].to_list()
        payloads = [{}]  # payloadを使う際は、{"city": "Berlin"}のように辞書で指定。現在は利用していない。
        qdrant_manager.add_vectors(ids, vectors, payloads)

    # search
    search_id = 50
    print(f'検索対象(id={search_id}): {df_text.query(f"id == {search_id}").text.item()}')

    search_results = qdrant_manager.search_vectors(vectors[search_id], top_k=3)
    for rank, search_result in enumerate(search_results):
        text = df_text.query(f'id == {search_result.id}').text.item()
        score = round(search_result.score, 2)
        print(f' 検索結果(id={search_result.id}) rank:{rank + 1} score:{score} text:{text}')

if __name__ == '__main__':
    main()
