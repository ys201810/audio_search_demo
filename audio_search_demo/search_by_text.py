# coding=utf-8
from pathlib import Path
import settings
from sentence_embedder import SentenceEmbedder
from qdrant_manager import QdrantManager
import pyarrow as pa
import pyarrow.parquet as pq


def main():
    base_path = Path(__file__).resolve().parents[1]
    MOVIE_NAME = settings.MOVIE_NAME

    parquet_file = base_path / 'data' / 'text' / f'{MOVIE_NAME}.parquet'
    if parquet_file.exists():
        table_loaded = pq.read_table(parquet_file)
        df_text = table_loaded.to_pandas()
    else:
        print(f'please make {parquet_file.name}.parquet using make_embeddings_db.py first.')
        exit(1)

    EMBEDDING_MODEL = settings.EMBEDDING_MODEL
    sentence_embedder = SentenceEmbedder(EMBEDDING_MODEL)
    question = '和室はありますか？'
    embedding_vectors = sentence_embedder.get_embedding_vector([question])
    print(f'質問:{question}')

    QDRANT_URL = settings.QDRANT_URL
    qdrant_manager = QdrantManager(url=QDRANT_URL, collection_name=MOVIE_NAME)
    search_results = qdrant_manager.search_vectors(vector=embedding_vectors[0], top_k=3)

    for rank, search_result in enumerate(search_results):
        text = df_text.query(f'id == {search_result.id}').text.item()
        start = df_text.query(f'id == {search_result.id}')[['start', 'end']].iloc[0]['start']
        end = df_text.query(f'id == {search_result.id}')[['start', 'end']].iloc[0]['end']
        score = round(search_result.score, 2)
        print(f' 検索結果(id={search_result.id}) rank:{rank + 1} score:{score} start:{start} end:{end} text:{text}')


if __name__ == '__main__':
    main()
