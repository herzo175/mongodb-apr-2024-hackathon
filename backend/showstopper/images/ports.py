from abc import ABC, abstractmethod
from typing import List


class ImageEmbedder(ABC):
    @abstractmethod
    def embed_images(self, images: List[str]) -> List[List[float]]:
        raise NotImplementedError

    @abstractmethod
    def embed_text(self, text: List[str]) -> List[List[float]]:
        raise NotImplementedError


class ImageCaptioner(ABC):
    @abstractmethod
    def caption_image(self, image: str) -> str:
        raise NotImplementedError
