from abc import ABC, abstractmethod
from datetime import time
from typing import List, Tuple

from showstopper.video.model import CombinedShot, VideoFrame


class VideoSplitter(ABC):
    @abstractmethod
    def create_video_frames(
        self, source_video_filename: str, output_dir: str, fps: int
    ) -> List[VideoFrame]:
        raise NotImplementedError


class VideoSplicer(ABC):
    @abstractmethod
    def trim_video_with_windows(
        self,
        source_video_file: str,
        output_video_file: str,
        timestamp_windows: List[Tuple[time, time]],
    ):
        raise NotImplementedError


class VideoVectorDatastore(ABC):
    @abstractmethod
    def save_video_shots(self, video_id: str, shots: List[CombinedShot]):
        raise NotImplementedError

    @abstractmethod
    def get_video_shots(
        self, video_id: str, query_embeddings: List[float]
    ) -> List[CombinedShot]:
        raise NotImplementedError
