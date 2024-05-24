from typing import List
import pysrt

from showstopper.audio.model import DialougeSegment
from showstopper.audio.ports import AudioTranscriber


def generate_subtitles_from_audio(
    input_audio_filepath: str, transcriber: AudioTranscriber
) -> List[DialougeSegment]:
    transcript = transcriber.generate_audio_transcript(input_audio_filepath)

    return [
        DialougeSegment(
            start_time=line.start.to_time(), end_time=line.end.to_time(), text=line.text
        )
        for line in pysrt.from_string(transcript)
    ]
