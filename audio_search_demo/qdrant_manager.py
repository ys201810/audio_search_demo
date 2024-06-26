# coding=utf-8
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

class QdrantManager:
    def __init__(self, url: str, collection_name: str):
        # Create a client
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name

    def create_collection(self, dim: int):
        # Create a collection
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=dim, distance=Distance.DOT),
            )
        else:
            print(f'Collection {self.collection_name} already exists')

    def add_vectors(self, ids: list, vectors: list, payloads: list):
        # make points
        points = []
        payload_value = {}  # payloadを利用する場合は、payloadsを利用
        for id, vector in zip(ids, vectors):  # zip(ids, vectors, payloads)
            points.append(PointStruct(id=id, vector=vector, payload=payload_value))  # payloadを使う際は、payloadを指定。
        # Insert vectors
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )
        print(operation_info)

    def search_vectors(self, vector: list, top_k: int):
        search_results = self.client.search(
            collection_name=self.collection_name, query_vector=vector, limit=top_k
        )

        return search_results

