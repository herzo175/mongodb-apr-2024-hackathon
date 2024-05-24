from typing import List

from numpy.linalg import norm
from numpy import dot

from showstopper.images.ports import ImageEmbedder


def images_same(emb_1: List[float], emb_2: List[float], similarity_threshold: float):
    cos_sim = dot(emb_1, emb_2) / (norm(emb_1) * norm(emb_2))
    # print("cos sim:", cos_sim)

    return cos_sim >= similarity_threshold


def generate_image_embeddings(image_paths: List[str], embedder: ImageEmbedder):
    return embedder.embed_images(image_paths)
