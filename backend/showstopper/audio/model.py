from datetime import time
from pydantic import BaseModel


class DialougeSegment(BaseModel):
    start_time: time
    end_time: time
    text: str
