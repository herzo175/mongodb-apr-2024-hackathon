import os
import tempfile
from typing import List

from showstopper.audio.ports import AudioTranscriber
from showstopper.audio.subtitles import generate_subtitles_from_audio
from showstopper.images.ports import ImageEmbedder
from showstopper.video.model import CombinedShot
from showstopper.video.ports import VideoSplitter
from showstopper.video.splicing import combine_shot_dialouge_windows
from showstopper.video.splitting import cut_video_shots, generate_video_frames


def generate_video_shots(
    input_video_filepath: str,
    video_splitter: VideoSplitter,
    image_embedder: ImageEmbedder,
    audio_transcriber: AudioTranscriber,
) -> List[CombinedShot]:
    with tempfile.TemporaryDirectory() as tempdir:
        audio_out = os.path.join(tempdir, "audio.mp3")

        video_splitter.split_audio_video(input_video_filepath, audio_out)

        frames_dir = os.path.join(tempdir, "frames")
        os.mkdir(frames_dir)

        frames = generate_video_frames(input_video_filepath, frames_dir, video_splitter)

        shots = cut_video_shots(frames, 0.85, image_embedder)
        transcript = generate_subtitles_from_audio(audio_out, audio_transcriber)

    return combine_shot_dialouge_windows(
        dialouge=transcript,
        shots=shots,
    )
