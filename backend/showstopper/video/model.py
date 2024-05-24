from datetime import time
from typing import List, Optional
from pydantic import BaseModel

from showstopper.audio.model import DialougeSegment


class VideoFrame(BaseModel):
    index: int
    file_path: str
    start_time: time
    end_time: time


class VideoShot(BaseModel):
    start_frame: VideoFrame
    end_frame: VideoFrame
    image_embedding: List[float]


class CombinedShot(BaseModel):
    start_time: time
    end_time: time
    dialouge: Optional[str] = None
    image_embedding: List[float]
