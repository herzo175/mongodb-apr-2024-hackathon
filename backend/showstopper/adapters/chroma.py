import json
import uuid
from datetime import time
from typing import List, Optional

import chromadb
from openai import BaseModel

from showstopper.video.model import CombinedShot
from showstopper.video.ports import VideoVectorDatastore


class CombinedShotDocument(BaseModel):
    video_id: str
    start_time: time
    end_time: time
    dialouge: Optional[str]


class ChromaAdapter(VideoVectorDatastore):
    def __init__(self):
        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(name="videos")

    def save_video_shots(self, video_id: str, shots: List[CombinedShot]):
        self.collection.add(
            ids=[str(uuid.uuid4()) for shot in shots],
            embeddings=[shot.image_embedding for shot in shots],
            metadatas=[{"video_id": video_id} for _ in shots],
            documents=[shot.model_dump_json() for shot in shots],
        )

    def get_video_shots(self, video_id: str, query_embeddings: List[float]):
        results = self.collection.query(
            query_embeddings=[query_embeddings],
            where={"video_id": video_id},
            n_results=20,
        )

        return [CombinedShot(**json.loads(doc)) for doc in results["documents"][0]]
